import json

from entity import Entity
from tile import Tile
from world import TileXY, World, worlds

def load_world(world_id, w):
  assert w["version"] == "0.1.0"
  tiles = []
  for row in w["tiles"]:
    row_tiles = []
    for t in row:
      row_tiles.append(Tile.fromJSON(t))
    tiles.append(row_tiles)

  entities = [Entity.fromJSON(e) for e in w["entities"]]

  spawn_points = {spawn_id:
    TileXY(spawn_tileXY["block_x"], spawn_tileXY["block_y"])
    for spawn_id, spawn_tileXY in w["spawn_points"].items()}
  worlds[world_id] = World(world_id, tiles, entities, spawn_points)

def load_file(world_id):
  with open(f"{world_id}.json") as f:
    load_world(world_id, json.load(f))

def load_worlds():
  load_file("starting_world")
  load_file("second_world")

