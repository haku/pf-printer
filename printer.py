from contextlib import AbstractContextManager
from types import TracebackType
from typing import List
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
from rich.style import Style
from rich.text import Text
from stransi.attribute import Attribute
import rich.box
import stransi

from args import ARGS
from udchar import Udchars

ARGS.add_argument("--width", dest='text_width', type=int)
ARGS.add_argument("--details", dest='show_details', action="store_true")
ARGS.add_argument("--preview", dest='print_preview', action="store_true")
ARGS.add_argument("--profile", dest='print_profile', default="TM-T88II")
ARGS.add_argument("--printer", dest='print_addr')
ARGS.add_argument("--font", dest='print_font', choices=['a', 'b'], default='b')


TITLE_FONT = 'a'

# in-band signalling to track font changes since terminals only have one font size.
TITLE_MARKER = "␁"
NORMAL_MARKER = "␂"

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

  def __init__(self, print_addr=None):
    Paragraph.new_line = False
    ListElement.new_line = False
    ListItem.new_line = False

    self.print_addr = print_addr or ARGS.print_addr

    if ARGS.text_width:
      self.width = ARGS.text_width
    else:
      p = printer.Dummy(profile=ARGS.print_profile)
      self.width = p.profile.get_columns(ARGS.print_font)
    if self.width < 10:
      raise Exception(f"invalid width: {self.width}")

    self.title_width = min(self.width, p.profile.get_columns(TITLE_FONT))
    self.format_to_print = ARGS.print_preview or self.print_addr

    self.renderables = []

    self.console = Console(
        force_terminal=True,
        width=self.width,
        highlight=False,
        markup=False,
        no_color=True,
        )

    self.render_called = False

  def __enter__(self):
    return self

  def __exit__(self, exc_type: type[BaseException] | None, exc_value:
               BaseException | None, traceback: TracebackType | None) -> None:
    if not self.render_called:
      print(self.render(), end="")

  @staticmethod
  def html_to_md(html):
    if not html or html == '<p></p>':
      return None
    html = html.replace('\n', '')
    return markdownify(html, strip=['hr'])

  def println(self):
    self.print(" ")  # empty string is falsey and gets ignored.

  def print(self, text):
    if not text:
      return

    if isinstance(text, str):
      self.renderables.append(Segments([Segment(text), Segment.line()]))
    elif isinstance(text, Segments):
      self.renderables.append(text)
    else:
      raise Exception(f"can not print type {type(text)}: {text}")

  def print_title(self, text: str | List[str | Udchars]):
    page_width = self.title_width if self.format_to_print else self.width
    text_width = self.count_chars(text)
    pad_width = int((page_width - text_width) / 2)

    segs = [Segment(' ' * pad_width)] + self.segment_wrap(text) + [Segment.line()]
    if self.format_to_print:
      segs.insert(0, Segment(TITLE_MARKER))
      segs.append(Segment(NORMAL_MARKER, style=Style(bold=True)))
    self.renderables.append(Segments(segs))

  def print_html(self, html):
    md = self.html_to_md(html)
    if not md:
      return
    self.print_markdown(md)

  def print_markdown(self, markup):
    md = Markdown(markup)
    md.elements["table_open"] = MyTableElement
    self.renderables.append(md)

  def print_hr(self):
    # ─ should get converted to cp437/0xc4
    self.renderables.append(Rule(characters='─'))

  def print_item(self, marker: str | List[str | Udchars], text):
    if not text:
      return
    self.print(self.render_item(marker, text))

  def render_item(self, marker: str | List[str | Udchars], text):
    marker_width = self.count_chars(marker)
    opts = self.console.options.update_width(self.width - marker_width)
    lines = self.console.render_lines(text, options=opts, pad=False)
    ret = []

    ret.extend(self.segment_wrap(marker))
    ret.extend(lines.pop(0))
    ret.append(NewLine())

    for l in lines:
      ret.append(Segment(' ' * marker_width))
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

  def count_chars(self, thing: str | List[str | Udchars]):
    if isinstance(thing, list):
      return sum([len(a) for a in thing])
    return len(thing)

  def segment_wrap(self, things: str | List[str | Udchars]):
    if isinstance(things, list):
      return[Segment(a) if isinstance(a, str) else a for a in things]
    return [Segment(things) if isinstance(things, str) else things]

  def render(self):
    self.render_called = True
    preview = []

    p = None
    if ARGS.print_preview:
      p = printer.Dummy(profile=ARGS.print_profile)
    elif self.print_addr:
      p = printer.Network(self.print_addr, profile=ARGS.print_profile)

    if p:
      p.set_with_default(font=ARGS.print_font)

    self.render_renderables(self.renderables, p, preview)

    if ARGS.print_preview:
      preview.append(p.output)
    elif self.print_addr:
      p.cut()

    return "".join(preview)

  def render_renderables(self, renderables, printer, preview):
    for r in renderables:
      if isinstance(r, Segments):
        self.render_segments(r.segments, printer, preview)
      else:
        self.render_rich([r], printer, preview)

  def render_segments(self, segments: List[Segments], printer, preview):
    for s in segments:
      if isinstance(s, Udchars):
        self.render_udchars(s, printer, preview)
      elif isinstance(s, Segment):
        self.render_rich([Segments([s])], printer, preview)
      else:
        self.render_rich([s], printer, preview)

  def render_udchars(self, udchars: Udchars, printer, preview):
    if printer:
      udchars.print_to_printer(printer, "b")
    else:
      preview.append(udchars.placeholder)

  def render_rich(self, renderables: List, printer, preview):
    with self.console.capture() as cap:
      for r in renderables:
        self.console.print(r)

    if printer:
      self.ansi_to_escpos(cap.get(), printer)
    else:
      preview.append(cap.get())

  def ansi_to_escpos(self, ansi, printer):
    decoded = stransi.Ansi(ansi)
    for i in decoded.instructions():
      if isinstance(i, str):
        if i.startswith(TITLE_MARKER):
          printer.set(font=TITLE_FONT)
          i = i[1:]
        elif i.startswith(NORMAL_MARKER):
          printer.set(font=ARGS.print_font)
          i = i[1:]

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
