"""Defines functions to load worlds from file."""
import json
import os

from world import World


def load_world(world_id, world_dict):
    """Register a world given by world_dict with the given world_id."""
    World.register_world(world_id, World.from_json(world_dict))


def load_file(world_id):
    """Register the world with the given world_id from a JSON file."""
    with open(f"worlds/{world_id}.json") as file:
        load_world(world_id, json.load(file))


def load_worlds():
    """Register all worlds in the folder."""
    with os.scandir("worlds") as files:
        for entry in files:
            load_file(entry.name[:-5])
