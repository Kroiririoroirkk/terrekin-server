"""The entry point for the server."""
import asyncio
from signal import signal, SIGINT
import sys
import time
import uuid
import websockets
from websockets.exceptions import ConnectionClosed

from battle import MoveChoice
from collision import block_movement
from config import Config
from entitybasic import EntityEventContext, EntityUpdateContext
import game
from geometry import Direction, Vec
from player import Player
from tilebasic import Tile, TileEventContext
from util import Util
from world import World
from loadworld import load_worlds

import entity  # Just to register the entities declared in entity.py
import tile  # Just to register the tiles declared in tile.py
del entity
del tile


running_game = game.Game()


load_worlds()


async def run(ws, path):
    """Run the WebSocket server."""
    del path  # Unused
    try:
        username = await ws.recv()
    except ConnectionClosed:
        return
    try:
        player = running_game.get_player(username)
        print("Returning user: " + username)
        print("Connecting from: "
              + ws.remote_address[0] + ":" + str(ws.remote_address[1]))
        player.ws = ws
        player.online = True
        world = World.get_world_by_id(player.world_id)
        await Util.send_world(ws, world, player.pos)
        if running_game.player_in_battle(username):
            battle = running_game.get_battle_by_username(username)
            c_id = player.combatant_id
            await Util.send_battle_start(ws, c_id.side)
            await Util.send_battle_status(ws, battle, c_id.side)
            await Util.send_move_request(ws, c_id.combatant_uuid)
    except ValueError:
        print("New user: " + username)
        print("Connecting from: "
              + ws.remote_address[0] + ":" + str(ws.remote_address[1]))
        world_id = "starting_world"
        spawn_id = "center_spawn"
        world = World.get_world_by_id(world_id)
        spawn_pos = world.spawn_points[spawn_id].to_spawn_pos()
        player = Player(
            username, spawn_pos, Vec(0, 0), Direction.DOWN, ws, world_id)
        running_game.add_player(player)
        await Util.send_world(ws, world, spawn_pos)
    try:
        async for message in ws:
            await parseMessage(message, username, ws)
    except ConnectionClosed:
        player.online = False


async def parseMessage(message, username, ws):
    """Handle a message from a client."""
    player = running_game.get_player(username)
    world = World.get_world_by_id(player.world_id)
    if message.startswith("move|") or message.startswith("fastmove|"):
        if running_game.player_in_battle(username) or player.talking_to:
            return
        multiplier = 1
        if message.startswith("fastmove|"):
            multiplier = Config.SPEED_MULTIPLIER
        parts = message.split("|")
        direction = parts[1]
        dir_vec = sum([
            Vec.vec_from_direction_str(char)
            for char in set(direction)], Vec(0, 0))
        if dir_vec:
            player.facing = Direction.str_to_direction(direction[-1])
            start_pos = player.pos
            start_tiles = player.get_tiles_touched()
            now = time.monotonic()
            dt = min(now - player.time_of_last_move, Config.MAX_MOVE_DT)
            player.time_of_last_move = now
            offset = dir_vec * (Config.PLAYER_SPEED * dt * multiplier)
            player.pos += offset
            tile_coords_touching = player.get_tiles_touched()
            wall_tiles = [
                tile_coord for tile_coord in tile_coords_touching
                if world.get_tile(tile_coord).blocks_movement]
            if wall_tiles:
                wall_tiles = [tile_coord.to_pos() for tile_coord in wall_tiles]
                wall_tiles.sort(
                    key=lambda tile_pos:
                    tile_pos.dist_to(player.pos))
                for wall_tile in wall_tiles:
                    block_movement(Tile.get_bounding_box(wall_tile),
                                   start_pos, player)
                tile_coords_touching = player.get_tiles_touched()
            wall_entities = [
                entity for entity in world.entities
                if entity.blocks_movement
                and player.is_touching(entity)]
            if wall_entities:
                wall_entities.sort(
                    key=lambda wall_entity:
                    wall_entity.pos.dist_to(player.pos))
                for wall_entity in wall_entities:
                    block_movement(wall_entity.get_bounding_box(),
                                   start_pos, player)
            tile_coords_moved_on = [
                tile_coord for tile_coord in tile_coords_touching
                if tile_coord not in start_tiles]
            for tile_coord in tile_coords_moved_on:
                tile_moved_on = world.get_tile(tile_coord)
                await tile_moved_on.on_move_on(TileEventContext(
                    game=running_game,
                    ws=ws,
                    username=username,
                    world=world,
                    player=player,
                    tile_pos=tile_coord.to_pos()), start_pos)
            await Util.send_moved_to(ws, player.pos)
    elif message.startswith("interact"):
        if running_game.player_in_battle(username):
            return
        if player.talking_to:
            await player.talking_to.on_interact(EntityEventContext(
                game=running_game,
                ws=ws,
                username=username,
                world=world,
                player=player))
        else:
            for tile_coord in player.get_tiles_touched():
                tile_interacted = world.get_tile(tile_coord)
                await tile_interacted.on_interact(TileEventContext(
                    game=running_game,
                    ws=ws,
                    username=username,
                    world=world,
                    player=player,
                    tile_pos=tile_coord.to_pos()))
            for entity_interacted in player.get_entities_can_interact(world):
                await entity_interacted.on_interact(EntityEventContext(
                    game=running_game,
                    ws=ws,
                    username=username,
                    world=world,
                    player=player))
            for player_in_game in running_game.players:
                if (player_in_game.world_id == player.world_id
                        and player_in_game.is_touching(player)
                        and player_in_game.username != username):
                    await Util.send_tag(
                        running_game, username, player_in_game.username)
    elif message.startswith("getupdates"):
        if running_game.player_in_battle(username):
            return
        await Util.send_players(running_game, ws, username, player.world_id)
        await Util.send_entities(ws, world)
    elif message.startswith("dialoguechoose"):
        if running_game.player_in_battle(username):
            return
        parts = message.split("|")
        entity_name = parts[1]
        entity_speaking_to = world.get_entity(entity_name)
        try:
            await entity_speaking_to.on_dialogue_choose(EntityEventContext(
                game=running_game,
                ws=ws,
                username=username,
                world=world,
                player=player
            ), int(parts[2]))
        except ValueError:
            pass
    elif message.startswith("battlemove"):
        battle = running_game.get_battle_by_username(username)
        if not battle:
            return
        parts = message.split("|")
        try:
            combatant_uuid = uuid.UUID(parts[1])
            if combatant_uuid != player.combatant_id.combatant_uuid:
                raise ValueError
            move = player.moves[int(parts[2])]
            target_uuid = uuid.UUID(parts[3])
            move_choice = MoveChoice(
                move,
                battle.get_combatant_id_by_uuid(target_uuid))
            winning_side = battle.process_player_move(move_choice)
            c_id = player.combatant_id
            if not winning_side:
                await Util.send_move_request(ws, c_id.combatant_uuid)
                await Util.send_battle_status(ws, battle, c_id.side)
            elif winning_side is c_id.side:
                await Util.send_battle_end(ws)
                running_game.del_battle_by_username(username)
            else:
                await Util.send_battle_end(ws)
                await Util.send_death(ws)
                running_game.del_battle_by_username(username)
                player.respawn()
                await Util.send_world(
                    ws, World.get_world_by_id(player.world_id), player.pos)
        except ValueError:
            pass


async def update_loop():
    """Update entities in player-inhabited worlds in an infinite loop."""
    then = time.monotonic()
    while True:
        now = time.monotonic()
        dt = now - then
        then = now
        for world_id in set(
                p.world_id for p in running_game.players):
            world = World.get_world_by_id(world_id)
            for ent in world.entities:
                ent.update(EntityUpdateContext(
                    game=running_game,
                    world=world,
                    dt=dt))
        for player in running_game.players:
            player.update(EntityUpdateContext(
                game=running_game,
                world=World.get_world_by_id(player.world_id),
                dt=dt))
        await asyncio.sleep(Config.UPDATE_DT)

start_server = websockets.serve(run, "0.0.0.0", Config.WSPORT)


def cleanup(sig, frame):
    """Handle a SIG_INTERRUPT, i.e. when Ctrl+C is pressed."""
    del sig, frame  # Unused
    print("Exiting...")
    sys.exit(0)


signal(SIGINT, cleanup)


print("WebSocket server starting! Press CTRL-C to exit.")
loop = asyncio.get_event_loop()
loop.create_task(update_loop())
loop.run_until_complete(start_server)
loop.run_forever()
