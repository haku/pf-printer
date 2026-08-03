#!/usr/bin/env python

import requests

import printer
import rdata
from args import ARGS
from formatting import space

def print_recipe(data, opts, printer):
  data = rdata.ensure(data)

  printer.print_title(f"{data['id']}: {data['name']}");

  for num, step in enumerate(data['steps']):
    printer.println()

    heading = [i['note'] for i in step['ingredients'] if i['is_header']]
    if heading:
      heading = f": {space(*heading)}"

    printer.print(space(f"Step {num}", heading))

    for ing in step['ingredients']:
      if ing['is_header']:
        continue

      amt = space(
          f"{ing['amount']:g}" if ing['amount'] else None,
          ing['unit']['name'])
      amt = f"**{amt}**" if amt else None

      note = ing['note']
      note = f"({note})" if note else None

      printer.print_markdown(space(
        "*",
        amt,
        ing['food']['name'],
        note,
        ))

    #printer.print(step['instruction'])
    printer.print_html(step['instructions_markdown'])

if __name__ == "__main__":
  ARGS.add_argument("--url", required=True)
  ARGS.add_argument("--token", required=True)

  req = requests.get(ARGS.url, headers={"Authorization": f"Bearer {ARGS.token}"})
  data = req.json()
  data = rdata.to_rdict(data)
  with printer.Printer() as p:
    print_recipe(data, None, p)
