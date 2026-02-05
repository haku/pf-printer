import argparse
import json
import pathlib
import re
from collections import defaultdict

from markdownify import markdownify
from rich.console import Console
from rich.markdown import Markdown
from rich.markdown import Paragraph
from rich.markdown import ListElement
from rich.markdown import ListItem


class Args:
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("--json",  type=pathlib.Path, required=True)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()

    self.json_path = args.json
    self.show_details = args.details

ARGS = Args()


class RDict(dict):
  def __missing__(self, key):
    return RDict()
  def __str__(self):
    return ""
  def __repr__(self):
    return ""

def to_rdict(d):
  if isinstance(d, dict):
    return RDict({k: to_rdict(v) for k, v in d.items()})
  if isinstance(d, list):
    return [to_rdict(i) for i in d]
  else:
    return d

def read_json_file(path):
  with open(path, 'r') as f:
    data = json.load(f)
  return to_rdict(data)

def read_json():
  with open(ARGS.json_path, 'r') as f:
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


class Printer:

  def __init__(self):
    Paragraph.new_line = False
    ListElement.new_line = False
    ListItem.new_line = False
    self.console = Console(highlight=False, no_color=True)

  @staticmethod
  def html_to_md(html):
    html = remove_macros(html)
    if not html or html == '<p></p>':
      return None
    html = html.replace('\n', '')
    return markdownify(html, strip=['hr'])

  def print(self, text):
    self.console.out(text)

  def print_html(self, html):
    md = self.html_to_md(html)
    if not md:
      return
    self.console.print(Markdown(md))

  def print_hr(self):
    self.console.print(Markdown('---'))

  def print_heading_and_html(self, things):
    for heading, html in things:
      md = self.html_to_md(html)
      if not md:
        continue
      self.console.print(Markdown('---'))
      self.console.out(heading)
      self.console.print(Markdown(md))
