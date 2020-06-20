"""Defines the TileCoord class."""
from collections import namedtuple

from config import Config
from geometry import Vec


class TileCoord(namedtuple("TileCoord", ["block_x", "block_y"])):
    """The TileCoord represents a position in the tile grid.

    It is a tuple of two whole numbers which are both nonnegative.
    """

    def to_spawn_pos(self):
        """Get the position in the tile in which the player spawns."""
        offset = (Config.BLOCK_WIDTH-Config.PLAYER_WIDTH)/2
        return Vec(self.block_x * Config.BLOCK_WIDTH + offset,
                   self.block_y * Config.BLOCK_WIDTH + offset)

    @staticmethod
    def pos_to_tile_coord(pos):
        """Return the TileCoord that a position Vec is in."""
        return TileCoord(int(pos.x) // Config.BLOCK_WIDTH,
                         int(pos.y) // Config.BLOCK_WIDTH)

    def to_pos(self):
        """Get the position of the upper-left corner of the tile."""
        return Vec(self.block_x * Config.BLOCK_WIDTH,
                   self.block_y * Config.BLOCK_WIDTH)
