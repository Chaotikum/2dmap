import argparse

parser = argparse.ArgumentParser(description='Compress tilesets.')
parser.add_argument('input', type=str, help='input JSON file')
parser.add_argument('output', type=str, help='output directory')
args = parser.parse_args()

import json
import os
import pathlib
import math
from PIL import Image

TILE_SIZE = 32
OUTPUT_COLUMNS = 10

def load(file):
  with open(file) as f:
    return json.load(f)

def save(file, data):
  with open(file, 'w') as f:
    json.dump(data, f, separators=(',', ':'))

data = load(args.input)
input_path = os.path.dirname(args.input)
output_png_relative = os.path.splitext(os.path.basename(args.input))[0] + ".png"
output_png = os.path.join(args.output, output_png_relative)
output_json = os.path.join(args.output, os.path.basename(args.input))
pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)

def to_box(offset, imagedimensions):
  (width, height) = imagedimensions
  tiles_per_row = width // TILE_SIZE
  x = offset % tiles_per_row
  y = offset // tiles_per_row
  return (x * TILE_SIZE, y * TILE_SIZE, (x+1) * TILE_SIZE, (y+1) * TILE_SIZE)

class Tileset:
  def __init__(self, data):
    self.data = data
    self.input_filename = os.path.join(input_path, data['image'])
    self.output_filename = os.path.join(args.output, data['image'])
    self.image = Image.open(self.input_filename)
    self.firstgid = data['firstgid']
    self.lastgid = self.firstgid + data['tilecount'] - 1
    assert data['tilewidth'] == TILE_SIZE
    assert data['tileheight'] == TILE_SIZE
    assert data['margin'] == 0
    assert data['spacing'] == 0

  def tile_image(self, id):
    offset = id - self.data['firstgid']
    box = to_box(offset, (self.data['imagewidth'], self.data['imageheight']))
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

def find_tile(tiles, id):
  for tile in tiles:
    if tile['id'] == id:
      return tile
  return None

tile_map = {}
tiles_data = []

for layer in data['layers']:
  if layer['type'] == 'tilelayer':
    for id in layer['data']:
      if id > 0:
        tile_map[id] = {}

im_width = OUTPUT_COLUMNS * TILE_SIZE
im_height = math.ceil(len(tile_map) / OUTPUT_COLUMNS) * TILE_SIZE
im = Image.new('RGBA', (im_width, im_height))
new_gid = 0
for gid in tile_map:
  new_gid += 1
  tile_map[gid] = new_gid
  tileset = get_tileset(gid)
  id = gid - tileset.firstgid
  if 'tiles' in tileset.data:
    tile_data = find_tile(tileset.data['tiles'], id)
    if tile_data:
      tile_data['id'] = new_gid - 1
      tiles_data.append(tile_data)
  tile = tileset.tile_image(gid)
  box = to_box(new_gid - 1, (im_width, im_height))
  im.paste(tile, box)
im.save(output_png)

for layer in data['layers']:
  if layer['type'] == 'tilelayer':
    layer['data'] = [tile_map[id] if id > 0 else 0 for id in layer['data']]

data['tilesets'] = [{
  "columns": 56,
  "firstgid": 1,
  "image": output_png_relative,
  "imageheight": im_height,
  "imagewidth": im_width,
  "margin": 0,
  "name": "map",
  "spacing": 0,
  "tilecount": len(tile_map),
  "tileheight": TILE_SIZE,
  "tilewidth": TILE_SIZE,
  "tiles": tiles_data
}]

save(output_json, data)
