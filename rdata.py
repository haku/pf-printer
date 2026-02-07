import json
import pathlib

from args import ARGS

ARGS.add_argument("--json", dest='json_path',  type=pathlib.Path)


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
