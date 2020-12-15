import argparse

parser = argparse.ArgumentParser(description='Edit JSON tile maps.')
parser.add_argument('--day', default=1, type=float, help="Set the opacity of all layers whose name ends with _day")
parser.add_argument('--night', default=0, type=float, help="Set the opacity of all layers whose name ends with _night")
parser.add_argument('--snow', default=0, type=float, help="Set the opacity of all layers whose name is weather_snow")
parser.add_argument('input', type=str, help='input JSON file')
parser.add_argument('output', type=str, help='output JSON file')
args = parser.parse_args()

import json

def load(file):
  with open(file) as f:
    return json.load(f)

def save(file, data):
  with open(file, 'w') as f:
    json.dump(data, f, separators=(',', ':'))

data = load(args.input)

for layer in data['layers']:
  name = layer['name']
  if name.endswith('_day'):
    layer['opacity'] = args.day
  if name.endswith('_night'):
    layer['opacity'] = args.night
  if name == 'waether_snow':
    layer['opacity'] = args.snow

save(args.output, data)
