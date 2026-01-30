import json
import re
from collections import defaultdict

from markdownify import markdownify
from rich.console import Console
from rich.markdown import Markdown
from rich.markdown import Paragraph
from rich.markdown import ListElement
from rich.markdown import ListItem


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

def space(*arr):
  return ' '.join([str(a) for a in arr if a])

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

def print_heading_and_html(things):
  console = Console()
  Paragraph.new_line = False
  ListElement.new_line = False
  ListItem.new_line = False

  for heading, html in things:
    html = remove_macros(html)
    if not html or html == '<p></p>':
      continue

    console.print(Markdown('---'))
    print(heading)
    html = html.replace('\n', '')
    md = markdownify(html, strip=['hr'])
    md = Markdown(md)
    console.print(md)
  
