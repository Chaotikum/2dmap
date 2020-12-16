import argparse

parser = argparse.ArgumentParser(description='Compress tilesets.')
parser.add_argument('input', type=str, help='input JSON file')
parser.add_argument('output', type=str, help='output directory')
args = parser.parse_args()

import json
import os
import pathlib
from PIL import Image

def load(file):
  with open(file) as f:
    return json.load(f)

def save(file, data):
  with open(file, 'w') as f:
    json.dump(data, f, separators=(',', ':'))

data = load(args.input)
input_path = os.path.dirname(args.input)
pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)

def to_box(offset, imagedimensions, tiledimensions):
  (width, height) = imagedimensions
  (tw, th) = tiledimensions
  tiles_per_row = width // tw
  x = offset % tiles_per_row
  y = offset // tiles_per_row
  return (x * tw, y * th, x * tw + tw, y * th + th)

class Tileset:
  def __init__(self, data):
    self.data = data
    self.input_filename = os.path.join(input_path, data['image'])
    self.output_filename = os.path.join(args.output, data['image'])
    self.image = Image.open(self.input_filename)
    self.firstgid = data['firstgid']
    self.lastgid = self.firstgid + data['tilecount']

  def tile_image(self, id):
    offset = id - self.data['firstgid']
    box = to_box(offset, (self.data['imagewidth'], self.data['imageheight']), (self.data['tilewidth'], self.data['tileheight']))
    return self.image.crop(box)



def load_tileset(tileset):
  image = tileset['image']
  im = Image.open(os.path.join(input_path, image))

tilesets = [Tileset(tileset) for tileset in data['tilesets']]

def get_tileset(gid):
  for tileset in tilesets:
    if tileset.firstgid <= gid and tileset.lastgid >= gid:
      return tileset
  return None

tile_map = {}

for layer in data['layers']:
  if layer['type'] == 'tilelayer':
    for id in layer['data']:
      if id > 0:
        tile_map[id] = 0

im = Image.new('RGBA', (320,320))
new_gid = 0
for gid in tile_map:
  print(gid)
  new_gid += 1
  tile_map[gid] = new_gid
  tileset = get_tileset(gid)
  tile = tileset.tile_image(gid)
  tile.save(os.path.join(args.output, f"{gid}.png"))
  im.paste(tile, to_box(new_gid - 1, (320,320), (32,32)))
im.save(os.path.join(args.output, 'map.png'))

save(os.path.join(args.output, os.path.basename(args.input)), data)
