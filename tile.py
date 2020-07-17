"""Defines classes for various tiles."""
import random

from battle import RandomMoveAICombatant
from geometry import Direction
from teleport import teleport
from tilebasic import (
    Tile, TilePlus, TileMetadata,
    register_tile, register_tile_plus)
from util import Util


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
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


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


@register_tile("carpet")
class Carpet(Tile):
    """Class for the carpet tile."""


@register_tile("rug")
class Rug(Tile):
    """Class for the rug tile."""


@register_tile("table")
class Table(Tile):
    """Class for the table tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


class ChairData(TileMetadata):
    """Stores the direction and ground tile of a chair tile."""

    def __init__(self, facing, ground_tile):
        """Initialize facing and ground_tile."""
        super().__init__()
        self.facing = facing
        self.ground_tile = ground_tile
        self.send_to_client = ["facing", "ground_tile"]

    @staticmethod
    def from_json(data):
        """Convert a dict representing a JSON object into ChairData."""
        return ChairData(Direction.str_to_direction(data["facing"]),
                         Tile.from_json(data["ground_tile"]))

    def to_json(self, is_to_client):
        """Serialize to JSON."""
        return {
            "facing": self.facing.direction_to_str(),
            "ground_tile": self.ground_tile.to_json(is_to_client)
        }


@register_tile_plus("chair", ChairData)
class Chair(TilePlus):
    """Class for the chair tile."""

    def __init__(self, data):
        """Initialize with the ability to block player movement."""
        super().__init__(data)
        self.blocks_movement = True


@register_tile("knickknack_shelf")
class KnickknackShelf(Tile):
    """Class for the knickknack shelf tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile_plus("left_door", PortalData)
class LeftDoor(TilePlus):
    """Class for the left door tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


@register_tile_plus("right_door", PortalData)
class RightDoor(TilePlus):
    """Class for the right door tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


@register_tile_plus("metal_left_door", PortalData)
class MetalLeftDoor(TilePlus):
    """Class for the metal left door tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


@register_tile_plus("metal_right_door", PortalData)
class MetalRightDoor(Tile):
    """Class for the metal right door tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


@register_tile("countertop")
class Countertop(Tile):
    """Class for the countertop tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


class StairData(TileMetadata):
    """Stores information about the destination of a stair tile."""

    def __init__(self, world_id, spawn_id):
        """Initialize with destination world_id and spawn_id."""
        super().__init__()
        self.world_id = world_id
        self.spawn_id = spawn_id

    @staticmethod
    def from_json(data):
        """Convert a dict representing a JSON object into StairData."""
        return StairData(data["world_id"], data["spawn_id"])

    def to_json(self, is_to_client):
        """Serialize to JSON."""
        return {
            "world_id": self.world_id,
            "spawn_id": self.spawn_id
        }


@register_tile_plus("stair_top_ascending", StairData)
class StairTopAscending(Tile):
    """Class for the stair (top, ascending) tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


@register_tile("stair_bottom_ascending")
class StairBottomAscending(Tile):
    """Class for the stair (bottom, ascending) tile."""


@register_tile("stair_top_descending")
class StairTopDescending(Tile):
    """Class for the stair (top, descending) tile."""


@register_tile_plus("stair_bottom_descending", StairData)
class StairBottomDescending(Tile):
    """Class for the stair (bottom, descending) tile."""

    async def on_move_on(self, event_ctx, player_start_pos):
        """Teleport players that move into the portal."""
        await teleport(event_ctx.game, event_ctx.ws, event_ctx.username,
                       event_ctx.player, self.data.world_id,
                       self.data.spawn_id)


@register_tile("couch")
class Couch(Tile):
    """Class for the couch tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("bed")
class Bed(Tile):
    """Class for the bed tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("lamp_nightstand")
class LampNightstand(Tile):
    """Class for the lamp nightstand tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("desk")
class Desk(Tile):
    """Class for the desk tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("bookcase")
class Bookcase(Tile):
    """Class for the bookcase tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("hung_up_clothes")
class HungUpClothes(Tile):
    """Class for the hung-up clothes tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("pile_of_clothes")
class PileOfClothes(Tile):
    """Class for the pile of clothes tile."""


@register_tile("player_roof")
class PlayerRoof(Tile):
    """Class for the player roof tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("shop_roof")
class ShopRoof(Tile):
    """Class for the shop roof tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("army_roof")
class ArmyRoof(Tile):
    """Class for the army roof tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("university_roof")
class UniversityRoof(Tile):
    """Class for the university roof tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("university_hospital_roof")
class UniversityHospitalRoof(Tile):
    """Class for the university hospital roof tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("roof")
class Roof(Tile):
    """Class for the roof tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("well")
class Well(Tile):
    """Class for the well tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("pavement")
class Pavement(Tile):
    """Class for the pavement tile."""


@register_tile("construction")
class Construction(Tile):
    """Class for the construction tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("trees")
class Trees(Tile):
    """Class for the trees tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True


@register_tile("garden")
class Garden(Tile):
    """Class for the garden tile."""

    def __init__(self):
        """Initialize with the ability to block player movement."""
        super().__init__()
        self.blocks_movement = True
