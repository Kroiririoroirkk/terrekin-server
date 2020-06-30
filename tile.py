"""Defines classes for various tiles."""
import random

from battle import RandomMoveAICombatant, Move, Species
from tilebasic import (
    Tile, TilePlus, TileMetadata,
    register_tile, register_tile_plus)
from util import Util
from world import World


@register_tile("grass")
class Grass(Tile):
    """Class for the grass tile."""


class WildGrassData(TileMetadata):
    """Stores information about the encounters in a wild grass tile."""

    def __init__(self, patch_id):
        """Initialize with the patch_id."""
        super().__init__()
        self.patch_id = patch_id

    @staticmethod
    def from_json(data):
        """Convert a dict representing a JSON object into a portal data."""
        return WildGrassData(data["patch_id"])

    def to_json(self, is_to_client):
        """Serialize to JSON."""
        return {"patch_id": self.patch_id}


@register_tile_plus("wild_grass", WildGrassData)
class WildGrass(TilePlus):
    """Class for the wild grass tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Chance of triggering a wild encounter."""
        patch = event_ctx.world.patches.get(self.data.patch_id)
        if not patch:
            return
        random_num = random.random()
        weight_total = sum(encounter.weight for encounter in patch)
        start = 0
        generated_encounter = None
        for encounter in patch:
            proportion = encounter.weight / weight_total
            if start <= random_num <= (start + proportion):
                generated_encounter = encounter
                break
            start += proportion
        if generated_encounter and generated_encounter.species:
            try:
                await event_ctx.game.create_battle(
                    event_ctx.username,
                    event_ctx.ws,
                    event_ctx.player,
                    RandomMoveAICombatant(
                        species=generated_encounter.species,
                        level=random.randint(generated_encounter.min_level,
                                             generated_encounter.max_level),
                        moves=generated_encounter.moves
                    )
                )
            except ValueError:
                pass


@register_tile("wall")
class Wall(Tile):
    """Class for the wall tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


class PortalData(TileMetadata):
    """Stores information about the destination of a portal tile."""

    def __init__(self, world_id, spawn_id, ground_tile):
        """Initialize with destination world_id and spawn_id."""
        super().__init__()
        self.world_id = world_id
        self.spawn_id = spawn_id
        self.ground_tile = ground_tile
        self.send_to_client = ["ground_tile"]

    @staticmethod
    def from_json(data):
        """Convert a dict representing a JSON object into PortalData."""
        return PortalData(data["world_id"], data["spawn_id"],
                          Tile.from_json(data["ground_tile"]))

    def to_json(self, is_to_client):
        """Serialize to JSON."""
        return {
            "world_id": self.world_id,
            "spawn_id": self.spawn_id,
            "ground_tile": self.ground_tile.to_json(is_to_client)
        }


@register_tile_plus("portal", PortalData)
class Portal(TilePlus):
    """Class for the portal tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        world_id = self.data.world_id
        world = World.get_world_by_id(world_id)
        spawn_id = self.data.spawn_id
        event_ctx.player.world_id = world_id
        event_ctx.player.pos = world.spawn_points[spawn_id].to_spawn_pos()
        await Util.send_world(event_ctx.ws, world, event_ctx.player.pos)
        await Util.send_players(
            event_ctx.game, event_ctx.ws, event_ctx.username, world_id)


class SignData(TileMetadata):
    """Stores information about the text and ground tile of a sign tile."""

    def __init__(self, text, ground_tile):
        """Initialize and flag ground_tile as info sent to the client."""
        super().__init__()
        self.text = text
        self.ground_tile = ground_tile
        self.send_to_client = ["ground_tile"]

    @staticmethod
    def from_json(data):
        """Convert a dict representing a JSON object into SignData."""
        return SignData(data["text"], Tile.from_json(data["ground_tile"]))

    def to_json(self, is_to_client):
        """Serialize to JSON."""
        return {
            "text": self.text,
            "ground_tile": self.ground_tile.to_json(is_to_client)
        }


@register_tile_plus("sign", SignData)
class Sign(TilePlus):
    """Class for the sign tile."""

    async def on_interact(self, event_ctx):
        """Send the sign's text when player interacts with sign."""
        await Util.send_sign(event_ctx.ws, self)


@register_tile("deep_water")
class DeepWater(Tile):
    """Class for the deep water tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("shallow_water")
class ShallowWater(Tile):
    """Class for the shallow water tile."""


@register_tile("dirt")
class Dirt(Tile):
    """Class for the dirt tile."""


@register_tile("desert")
class Desert(Tile):
    """Class for the desert tile."""


@register_tile("lava")
class Lava(Tile):
    """Class for the lava tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("floor")
class Floor(Tile):
    """Class for the floor tile."""


@register_tile("indoor_wall")
class IndoorWall(Tile):
    """Class for the indoor wall tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("barrier")
class Barrier(Tile):
    """Class for the barrier tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True
