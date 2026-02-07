import io
import json
import pathlib
import re
import sys
from collections import defaultdict
from contextlib import AbstractContextManager
from types import TracebackType

from markdownify import markdownify
from rich.console import Console
from rich.console import ConsoleOptions
from rich.console import NewLine
from rich.console import RenderResult
from rich.markdown import ListElement
from rich.markdown import ListItem
from rich.markdown import Markdown
from rich.markdown import Paragraph
from rich.markdown import TableElement
from rich.segment import Segment
from rich.segment import Segments
from rich.rule import Rule
import rich.box

from escpos import printer
from stransi.attribute import Attribute
import stransi

from args import ARGS

ARGS.add_argument("--json", dest='json_path',  type=pathlib.Path)
ARGS.add_argument("--width", dest='text_width', type=int, default=56)
ARGS.add_argument("--details", dest='show_details', action="store_true")
ARGS.add_argument("--preview", dest='print_preview', action="store_true")
ARGS.add_argument("--printer", dest='print_profile', default="TM-T88II")


class RDict(dict):
  def __missing__(self, key):
    return RDict()
  def __str__(self):
    return ""
  def __repr__(self):
    return ""

def to_rdict(d):
  if isinstance(d, dict):
    return RDict({k: to_rdict(v) for k, v in d.items() if v is not None})
  if isinstance(d, list):
    return [to_rdict(i) for i in d]
  else:
    return d

def read_json_file(path):
  with open(path, 'r') as f:
    data = json.load(f)
  return to_rdict(data)

def read_json():
  with open(ARGS.get_required('json_path'), 'r') as f:
    data = json.load(f)
  return to_rdict(data)


def space(*arr, sep=" "):
  return sep.join([str(a) for a in arr if a])

def level(l):
  if not l['value']:
    return None
  return f"L{l['value']}"

def remove_macros(text):
  matches = re.finditer(r"@([^[]+)\[([^\]]+)\](\{[^}]+\})?", text)
  for m in reversed(list(matches)):
    a = m.group(1)
    b = m.group(2)
    c = m.group(3)
    if a == "Check":
      p = b.split('|')
      rep = p[0]
      if len(p) >= 2:
        rep += f"/{p[1]}"
    elif a == "UUID":
      if c:
        rep = c
      else:
        rep = b.rsplit('.', maxsplit=1)[1]
    elif a == "Localize":
      rep = ""
    elif a == "Damage":
      rep = b
    elif a == "Template":
      if c:
        rep = c
      else:
        p = b.split('|')
        rep = f"{p[0].replace('type:', '')}/{p[1]}"
    else:
      continue
    text = text[:m.start()] + rep + text[m.end():]
  return text


ASCII_SIMPLE_BOX = rich.box.Box(
    "    \n"
    "    \n"
    " -- \n"
    "    \n"
    "    \n"
    " -- \n"
    "    \n"
    "    \n",
    ascii=True,
)

class MyTableElement(TableElement):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
    for table in super().__rich_console__(console, options):
      #table.box = ASCII_SIMPLE_BOX
      table.box = rich.box.SIMPLE
      yield table


class Printer(AbstractContextManager):

  def __init__(self):
    Paragraph.new_line = False
    ListElement.new_line = False
    ListItem.new_line = False

    file = io.StringIO()
    self.console = Console(
        file=file,
        force_terminal=True,
        width=ARGS.text_width,
        highlight=False,
        markup=False,
        no_color=True,
        )

  def __enter__(self):
    return self

  def __exit__(self, exc_type: type[BaseException] | None, exc_value:
               BaseException | None, traceback: TracebackType | None) -> None:
    captured = self.console.file.getvalue()

    if ARGS.print_preview:
      p = printer.Dummy(profile=ARGS.print_profile)
      self.ansi_to_escpos(captured, p)
      print(p.output)
    else:
      print(captured)

  @staticmethod
  def html_to_md(html):
    html = remove_macros(html)
    if not html or html == '<p></p>':
      return None
    html = html.replace('\n', '')
    return markdownify(html, strip=['hr'])

  def print(self, text):
    self.console.print(text, emoji=False, markup=False)

  def print_html(self, html):
    md = self.html_to_md(html)
    if not md:
      return
    self.print_markdown(md)

  def print_markdown(self, markup):
    md = Markdown(markup)
    md.elements["table_open"] = MyTableElement
    self.console.print(md)

  def print_hr(self):
    # ─ should get converted to cp437/0xc4
    self.console.print(Rule(characters='─'))

  def render_item(self, marker, text):
    opts = self.console.options.update_width(ARGS.text_width - len(marker))
    lines = self.console.render_lines(text, options=opts, pad=False)
    ret = []

    ret.append(Segment(marker))
    ret.extend(lines.pop(0))
    ret.append(NewLine())

    for l in lines:
      ret.append(Segment(' ' * len(marker)))
      ret.extend(l)
      ret.append(NewLine())

    return Segments(ret)

  def print_heading_and_html(self, things):
    for heading, html in things:
      md = self.html_to_md(html)
      if not md:
        continue
      self.print_hr()
      self.print(heading)
      self.print_markdown(md)

  @staticmethod
  def ansi_to_escpos(ansi, printer):
    decoded = stransi.Ansi(ansi)
    # https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.set_with_default
    printer.set_with_default(font="b")
    for i in decoded.instructions():
      if isinstance(i, str):
        printer.text(i)
      elif isinstance(i, stransi.SetAttribute):
        # https://github.com/getcuia/stransi/blob/main/src/stransi/attribute.py
        if i.attribute == Attribute.NORMAL:
          printer.set(bold=False, underline=False)
        elif i.attribute == Attribute.BOLD:
          printer.set(bold=True)
        elif i.attribute == Attribute.UNDERLINE:
          printer.set(underline=True)
        elif i.attribute == Attribute.ITALIC:
          printer.set(bold=True)  # map italic to bold.
        else:
          raise Exception(f"unknown attribute {i.attribute}: {i}")
      else:
        raise Exception(f"unknown type {type(i)}: {i}")
