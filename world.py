"""Defines the World class."""
from collections import namedtuple
from typing import Dict

from battle import Move, Species
from cutscene import Cutscene
from entitybasic import Entity
from tilebasic import Empty, Tile
from tilecoord import TileCoord


_worlds: Dict[str, "World"] = {}


class Encounter(namedtuple("Encounter", [
        "species",
        "min_level",
        "max_level",
        "moves",
        "weight"
])):
    """Stores info for a possible WildGrass encounter."""

    @staticmethod
    def from_json(data):
        """Convert a dict representing a JSON object into an Encounter."""
        return Encounter(
            Species.get_by_id(data["species"]) if data["species"] else None,
            data["min_level"],
            data["max_level"],
            [Move.get_by_id(move) for move in data["moves"]],
            data["weight"])

    def to_json(self):
        """Serialize to JSON."""
        return {
            "species": self.species.id if self.species else None,
            "min_level": self.min_level,
            "max_level": self.max_level,
            "moves": [move.id for move in self.moves],
            "weight": self.weight
        }


class World:
    """The World class represents an area where the player can explore.

    Different Worlds are linked together through portals.
    """

    def __init__(self, tiles, entities, spawn_points, cutscenes, patches):
        """Initialize the World with its contents."""
        self.tiles = tiles
        self.entities = entities
        self.spawn_points = spawn_points
        self.cutscenes = cutscenes
        self.patches = patches

    def get_tile(self, tile_coord):
        """Get the tile positioned at the given TileCoord."""
        try:
            return self.tiles[tile_coord.block_y][tile_coord.block_x]
        except IndexError:
            return Empty()

    def get_entity(self, name):
        """Get the entity with the given name."""
        try:
            return next(
                entity for entity in self.entities
                if entity.name == name)
        except StopIteration:
            raise ValueError

    @staticmethod
    def from_json(world_dict):
        """Convert a dict representing a JSON object into a world."""
        if world_dict["version"] != "0.4.0":
            raise ValueError
        tiles = []
        for row in world_dict["tiles"]:
            row_tiles = []
            for tile in row:
                row_tiles.append(Tile.from_json(tile))
            tiles.append(row_tiles)

        entities = [
            Entity.from_json(entity) for entity in world_dict["entities"]]

        spawn_points = {
            spawn_id: TileCoord(
                spawn_tile_coord["block_x"],
                spawn_tile_coord["block_y"])
            for spawn_id, spawn_tile_coord
            in world_dict["spawn_points"].items()}

        cutscenes = [
            Cutscene.from_json(scene) for scene in world_dict["cutscenes"]]

        patches = {
            patch_id: [Encounter.from_json(encounter) for encounter in patch]
            for patch_id, patch
            in world_dict["patches"].items()}

        return World(tiles, entities, spawn_points, cutscenes, patches)

    def to_json_client(self, spawn_pos):
        """Convert a world to a dict which can be converted to a JSON string.

        This method is for data that will be sent to the client.
        """
        tiles_list = []
        for row in self.tiles:
            row_tiles = []
            for tile in row:
                row_tiles.append(tile.to_json(True))
            tiles_list.append(row_tiles)

        entity_list = [entity.to_json(True) for entity in self.entities]

        spawn_pos_obj = spawn_pos.to_json()

        cutscene_list = [
            cutscene.to_json(True) for cutscene in self.cutscenes]

        return {
            "version": "0.3.0",
            "tiles": tiles_list,
            "entities": entity_list,
            "spawn_pos": spawn_pos_obj,
            "cutscenes": cutscene_list
        }

    def to_json_save(self):
        """Convert a world to a dict which can be converted to a JSON string.

        This method is for data that will be saved to file.
        """
        tiles_list = []
        for row in self.tiles:
            row_tiles = []
            for tile in row:
                row_tiles.append(tile.to_json(False))
            tiles_list.append(row_tiles)

        entity_list = [entity.to_json(False) for entity in self.entities]

        spawn_point_list = {
            spawn_id: {"block_x": spawn_point.block_x,
                       "block_y": spawn_point.block_y}
            for spawn_id, spawn_point in self.spawn_points.items()}

        cutscene_list = [
            cutscene.to_json(False) for cutscene in self.cutscenes]

        patch_list = {
            patch_id: [encounter.to_json() for encounter in patch]
            for patch_id, patch in self.patches.items()}

        return {
            "version": "0.4.0",
            "tiles": tiles_list,
            "entities": entity_list,
            "spawn_points": spawn_point_list,
            "cutscenes": cutscene_list,
            "patches": patch_list
        }

    @staticmethod
    def get_world_by_id(world_id):
        """Get the World corresponding to a world_id."""
        world = _worlds.get(world_id)
        if not world:
            raise ValueError
        return world

    def get_world_id(self):
        """Get the world_id of a World."""
        try:
            return next(
                world_id for world_id, world in _worlds.items()
                if world == self)
        except StopIteration:
            raise ValueError

    @staticmethod
    def register_world(world_id, world):
        """Register a World with the given world_id."""
        if world_id in _worlds:
            raise ValueError
        _worlds[world_id] = world
