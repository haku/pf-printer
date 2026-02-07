from contextlib import AbstractContextManager
from types import TracebackType
import io

from escpos import printer
from markdownify import markdownify
from rich.align import Align
from rich.console import Console
from rich.console import ConsoleOptions
from rich.console import NewLine
from rich.console import RenderResult
from rich.markdown import ListElement
from rich.markdown import ListItem
from rich.markdown import Markdown
from rich.markdown import Paragraph
from rich.markdown import TableElement
from rich.rule import Rule
from rich.segment import Segment
from rich.segment import Segments
from stransi.attribute import Attribute
import rich.box
import stransi

from args import ARGS

ARGS.add_argument("--width", dest='text_width', type=int)
ARGS.add_argument("--details", dest='show_details', action="store_true")
ARGS.add_argument("--preview", dest='print_preview', action="store_true")
ARGS.add_argument("--profile", dest='print_profile', default="TM-T88II")
ARGS.add_argument("--printer", dest='print_addr')
ARGS.add_argument("--font", dest='print_font', choices=['a', 'b'], default='b')


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

    if ARGS.text_width:
      self.width = ARGS.text_width
    else:
      p = printer.Dummy(profile=ARGS.print_profile)
      self.width = p.profile.get_columns(ARGS.print_font)
    if self.width < 10:
      raise Exception(f"invalid width: {self.width}")

    file = io.StringIO()
    self.console = Console(
        file=file,
        force_terminal=True,
        width=self.width,
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
    elif ARGS.print_addr:
      p = printer.Network(ARGS.print_addr, profile=ARGS.print_profile)
      self.ansi_to_escpos(captured, p)
      p.cut()
    else:
      print(captured)

  @staticmethod
  def html_to_md(html):
    if not html or html == '<p></p>':
      return None
    html = html.replace('\n', '')
    return markdownify(html, strip=['hr'])

  def println(self):
    self.console.print("", emoji=False, markup=False)

  def print(self, text, style=None):
    if not text:
      return
    self.console.print(text, emoji=False, markup=False, style=style)

  def print_title(self, text):
    self.print(Align.center(text), style="bold")

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

  def print_item(self, marker, text):
    if not text:
      return
    self.print(self.render_item(f"{marker} ", text))

  def render_item(self, marker, text):
    opts = self.console.options.update_width(self.width - len(marker))
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
