"""Defines teleport to handle portal teleportation."""

from config import Config
from util import Util
from world import World


async def teleport(game, ws, username, player, world_id, spawn_id):
    """Change player's world and send new world to client."""
    if not player.portal_cooldown:
        world = World.get_world_by_id(world_id)
        player.world_id = world_id
        player.pos = world.spawn_points[spawn_id].to_spawn_pos()
        player.portal_cooldown = Config.PORTAL_COOLDOWN_DT
        await Util.send_world(ws, world, player.pos)
        await Util.send_players(
            game, ws, username, world_id)
