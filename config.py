"""Various configuration values for the game.

WSPORT: Port that the WebSocket server runs on.

BLOCK_WIDTH: Width and height of one in-game block, in pixels.

PLAYER_WIDTH: Width and height of player, in pixels.

PLAYER_SPEED: Speed of the player in pixels per second.

SPEED_MULTIPLIER: Ratio of fast-moving speed to regular speed.

MAX_MOVE_DT: The maximum time between move messages.
If the amount of time between two move messages is
greater than MAX_MOVE_DT, they are considered two separate
moves. Otherwise, they are considered a single move.

UPDATE_DT: Amount of seconds between entity-updating calls.
This is a lower bound.
"""


class Config:
    """Class that contains configuration values."""

    WSPORT = 8080
    BLOCK_WIDTH = 32
    PLAYER_WIDTH = 28
    PLAYER_SPEED = BLOCK_WIDTH*3
    SPEED_MULTIPLIER = 2
    MAX_MOVE_DT = 0.1
    UPDATE_DT = 0.1
