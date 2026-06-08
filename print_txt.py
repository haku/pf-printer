#!/usr/bin/env python

import printer
from args import ARGS


def print_txt(data, opts, printer):
  printer.print(data)

if __name__ == "__main__":
  ARGS.add_argument('filename')
  with open(ARGS.filename, 'r') as f:
    data = f.read()

  with printer.Printer() as p:
    print_text(data, None, p)
