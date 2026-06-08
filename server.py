#!/usr/bin/env python
# https://flask.palletsprojects.com/en/stable/quickstart/
# run: $ gunicorn server:app

from dataclasses import dataclass
from enum import Enum
from flask import Flask
from flask import abort
from flask import make_response
from flask import request
from typing import Dict
import json
import os
import uuid

import print_item
import print_tandoor
import print_txt
import printer
import rdata
import time


PRINTER_ADDR = os.environ["PRINTER_ADDR"]

HEADER_PRINT_TOKEN = "X-Print-Token"

class JobType(Enum):
  TEXT = 1;
  PF_CREATURE = 2;
  PF_ITEM = 3;
  PF_SPELL = 4;
  TANDOOR = 5;

JOB_CONTENT_TYPES = {
    "text/plain": JobType.TEXT,
    "application/vnd.tandoor.recipe": JobType.TANDOOR,
    "application/vnd.pathfinder.item": JobType.PF_ITEM,
}

# method params: raw_data: str, opts: dict, printer
JOB_FORMATTERS = {
    JobType.TEXT: print_txt.print_txt,
    JobType.TANDOOR: print_tandoor.print_recipe,
    JobType.PF_ITEM: print_item.print_item,
}

@dataclass
class Job:
  time: float
  typ: JobType
  opts: Dict[str, str]
  raw_data: str
# FIXME this will not work across multiple instances, not sure what best alt is.
JOB_CACHE: Dict[str, Job] = {}

def clean_job_cache():
  for i, j in list(JOB_CACHE.items()):
    if time.monotonic() - j.time > 15 * 60:
      del JOB_CACHE[i]

app = Flask(__name__)

@app.route("/")
def serve_root():
  return "i am a printer desu~"

@app.route("/print", methods=['POST'])
def serve_print():
  print_token = request.headers.get(HEADER_PRINT_TOKEN)
  if print_token:
    job = JOB_CACHE.get(print_token)
    if not job:
      abort(400, f"Unknown {HEADER_PRINT_TOKEN}")
    del JOB_CACHE[print_token]

    try:
      with printer.Printer(print_addr=PRINTER_ADDR) as p:
        fmtr(raw_data, job.opts, p)
      return
    except Exception as e:
      abort(500, f"Print failed: {str(e)}")

  content_type = request.headers.get("Content-Type")
  job_type = JOB_CONTENT_TYPES.get(content_type)
  if not job_type:
    abort(400, "Missing or unknown Content-Type.")

  fmtr = JOB_FORMATTERS.get(job_type)
  if not fmtr:
    abort(500, "Missing formatter.")

  raw_data = request.get_data(as_text=True)
  opts = {}  # TODO parse opts
  with printer.Printer() as p:
    fmtr(raw_data, opts, p)
    preview = p.render()

  job_id = str(uuid.uuid4())
  job = Job(time=time.monotonic(), typ=job_type, opts=opts, raw_data=raw_data)
  clean_job_cache()
  JOB_CACHE[job_id] = job

  resp = make_response(preview)
  resp.headers["Content-Type"] = "text/plain"
  resp.headers[HEADER_PRINT_TOKEN] = job_id
  return resp


if __name__ == "__main__":
  app.run()
