"""Utility methods to send messages to the client."""
import json
from websockets.exceptions import ConnectionClosed

from storeworld import world_to_client_json


class Util:
    """Contains the utility methods."""

    @staticmethod
    async def send_world(ws, world, spawn_pos):
        """See the world message under PROTOCOL.md for explanation."""
        await ws.send(f"world|{world_to_client_json(world, spawn_pos)}")

    @staticmethod
    async def send_moved_to(ws, pos):
        """See the movedto message under PROTOCOL.md for explanation."""
        await ws.send(f"movedto|{pos.x}|{pos.y}")

    @staticmethod
    async def send_sign(ws, sign):
        """See the signtext message under PROTOCOL.md for explanation."""
        await ws.send(f"signtext|{sign.data.text}")

    @staticmethod
    async def send_players(game, ws, player_username, world_id):
        """See the players message under PROTOCOL.md for explanation."""
        players_str = "|".join(
            f"{p.username}|{p.pos.x}|{p.pos.y}"
            for p in game.players
            if p.world_id == world_id
            and p.username != player_username)
        await ws.send("players|"+players_str)

    @staticmethod
    async def send_entities(ws, world):
        """See the entities message under PROTOCOL.md for explanation."""
        entities_str = "|".join(
            json.dumps(e.to_json(True), separators=(",", ":"))
            for e in world.entities)
        await ws.send("entities|"+entities_str)

    @staticmethod
    async def send_dialogue(ws, uuid, dialogue_text):
        """See the dialogue message under PROTOCOL.md for explanation."""
        await ws.send(f"dialogue|{uuid.hex}|{dialogue_text}")

    @staticmethod
    async def send_dialogue_choices(ws, uuid, lines):
        """See the dialoguechoice message under PROTOCOL.md for explanation."""
        await ws.send(f"dialoguechoice|{uuid.hex}|{'|'.join(lines)}")

    @staticmethod
    async def send_dialogue_end(ws, uuid):
        """See the dialogueend message under PROTOCOL.md for explanation."""
        await ws.send(f"dialogueend|{uuid.hex}")

    @staticmethod
    async def send_tag(game, tagging_player, tagged_player):
        """See the tag message under PROTOCOL.md for explanation."""
        message = f"tag|{tagging_player}|{tagged_player}"
        try:
            await game.get_player(tagging_player).ws.send(message)
        except ConnectionClosed:
            pass
        try:
            await game.get_player(tagged_player).ws.send(message)
        except ConnectionClosed:
            pass

    @staticmethod
    async def send_battle_start(ws, side):
        """See the battlestart message under PROTOCOL.md for explanation."""
        await ws.send(f"battlestart|{side.value}")

    @staticmethod
    async def send_move_request(ws, uuid):
        """See the battlemovereq message under PROTOCOL.md for explanation."""
        await ws.send(f"battlemovereq|{uuid.hex}")

    @staticmethod
    async def send_battle_status(ws, battle, side):
        """See the battlestatus message under PROTOCOL.md for explanation."""
        battle_str = json.dumps(battle.to_json(side),
                                separators=(",", ":"))
        await ws.send(f"battlestatus|{battle_str}")

    @staticmethod
    async def send_battle_end(ws):
        """See the battleend message under PROTOCOL.md for explanation."""
        await ws.send("battleend")

    @staticmethod
    async def send_death(ws):
        """See the death message under PROTOCOL.md for explanation."""
        await ws.send("death")
