import re

import dice
from formatting import com
from formatting import space

def actions(system):
  if system['actions']['value']:
    return parse_actions(system['actions']['value'])
  elif system['actionType']['value']:
    return parse_actions(system['actionType']['value'])
  elif system['time']['value']:
    return parse_actions(system['time']['value'])
  else:
    return '*'

def parse_actions(t):
  if t == 'reaction':
    return '<-'
  elif t == 'passive':
    return '-'
  elif t == "1 to 3":
    return '*/**/***'
  else:
    m = re.match(r"(\d+) *(minutes?|hours?|days?)", str(t))
    if m:
      return f"{m.group(1)}{m.group(2)[:1]}"

    try:
      return '*' * int(t)
    except ValueError:
      return t

def damage(d, add=None):
  if not d:
    return None
  amt = space(
    d['formula'],
    f"{d['dice']}{d['die']}" if d['die'] else None,
    )
  if not amt:
    return None

  if add:
    amt = dice.parse(amt)
    amt = amt.append(add)
    amt = space(*amt, sep="+")

  typ = com(d['kind'], d['type'], d['damageType'], d['category'])
  return f"{amt} ({typ})"

def level(l, letter="L"):
  if l['value'] is None:
    return None
  return f"{letter}{l['value']}"

def remove_macros_html(text):
  return remove_macros(text, lambda t: f"<strong>{t}</strong>")

def remove_macros(text, formatter=None):
  if not formatter:
    formatter = lambda t: t

  text = remove_at_macros(text, formatter)
  text = remove_slash_macros(text, formatter)
  return text

def remove_at_macros(text, formatter):
  matches = re.finditer(r"@([^[]+)\[([^\]]+)\](?:\{([^}]+)\})?", text)
  for m in reversed(list(matches)):
    # @a[b]{c}
    a = m.group(1)
    b = m.group(2)
    c = m.group(3)

    # @Check[reflex|dc:21]
    # @Check[fortitude|dc:33|basic|options:area-effect]
    if a == "Check":
      p = b.split('|')
      rep = p[0]
      if len(p) >= 2:
        rep += f"/{p[1]}"

    # @UUID[Compendium.pf2e.conditionitems.Item.Confused]
    # @UUID[Compendium.pf2e.spells-srd.Item.Illusory Disguise]
    # @UUID[Compendium.pf2e.actionspf2e.Item.Trip]{Trips}
    elif a == "UUID":
      if c:
        rep = c
      else:
        rep = b.rsplit('.', maxsplit=1)[1]

    # @Localize[PF2E.NPC.Abilities.Glossary.Push]
    elif a == "Localize":
      rep = ""

    # TODO decode these better
    # @Damage[(1d10+2)[piercing]]
    # @Damage[(@item.level)[bleed]]
    # @Damage[2d6[persistent,bleed]]
    # deals @Damage[18d6[poison]|options:area-damage] damage
    elif a == "Damage":
      rep = b

    # @Template[cone|distance:50]
    # @Template[emanation|distance:30]{30 feet}
    # in a @Template[type:cone|distance:30] take
    elif a == "Template":
      if c:
        rep = c
      else:
        p = b.split('|')
        rep = f"{p[0].replace('type:', '')}/{p[1]}"
    else:
      continue
    text = text[:m.start()] + formatter(rep) + text[m.end():]
  return text

def remove_slash_macros(text, formatter):
  matches = re.finditer(r"\[\[/([^ ]+)([^\]]+)]](?:\{([^}]+)\})?", text)
  for m in reversed(list(matches)):
    # [[/a b]]{c}
    a = m.group(1)
    b = m.group(2)
    c = m.group(3)

    # [[/gmr 1d4 #hours]]{1d4 hours}
    # [[/gmr 1d4 #Recharge Poison Breath]]{1d4 rounds}
    if a == "gmr":
      rep = c if c else b

    # [[/act trip]]
    # [[/act force-open dc=23]]{Forces Open}
    # [[/act grapple skill=diplomacy]]{Grapple}
    elif a == "act":
      rep = c if c else b

    # [[/br 2d4 #hours]]{2d4 hours}
    # [[/br 2d4 #Recharge Corrosive Breath or Double Breath]]{2d4 rounds}
    elif a == "br":
      rep = c if c else b

    # within [[/r 10d10 #Miles Off]] miles
    # additional [[/r {2d10}]]{2d10 damage} to that
    # with a [[/r 1d20+17 #Counteract]]{+17} counteract
    elif a == "r":
      if c:
        rep = c
      else:
        rep = b.split(' ')[0]

    else:
      continue
    text = text[:m.start()] + formatter(rep) + text[m.end():]
  return text
