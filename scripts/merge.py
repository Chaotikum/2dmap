import argparse

parser = argparse.ArgumentParser(description='Merge adjacent layers in JSON tile maps if they do not contain tiles in the same positions.')
parser.add_argument("--ignore", nargs="+", default=[], help="Leave layers untouched with the given names.")
parser.add_argument("--ignore-suffix", nargs="+", default=[], help="Leave layers untouched whose names end with the given suffixes.")
parser.add_argument('input', type=str, help='input JSON file')
parser.add_argument('output', type=str, help='output JSON file')
args = parser.parse_args()

def merge(a, b):
  if a['type'] != 'tilelayer' or b['type'] != 'tilelayer':
    return None
  if a['width'] != b['width'] or a['height'] != b['height'] or a['visible'] != b['visible'] or a['opacity'] != b['opacity']:
    return None
  if 'properties' in a or 'properties' in b:
    return None
  if any(a > 0 and b > 0 for (a,b) in zip(a['data'], b['data'])):
    return None
  a['data'] = [(a if a > 0 else b) for (a,b) in zip(a['data'], b['data'])]
  print(f"Integrated {b['name']} into {a['name']}")
  return a

import json

def load(file):
  with open(file) as f:
    return json.load(f)

def save(file, data):
  with open(file, 'w') as f:
    json.dump(data, f, separators=(',', ':'))

data = load(args.input)

layers = []
lastLayer = None

def ok(layer):
  name = layer['name']
  for ignore in args.ignore:
    if name == ignore:
      return False
  for suffix in args.ignore_suffix:
    if name.endswith(suffix):
      return False
  return True

for layer in data['layers']:
  if lastLayer:
    merged = None
    if ok(lastLayer) and ok(layer):
      merged = merge(layer, lastLayer)
    if merged:
      layer = merged
    else:
      layers.append(lastLayer)
  lastLayer = layer

layers.append(lastLayer)
data['layers'] = layers

save(args.output, data)
