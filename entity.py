"""Defines classes for various entities."""
from collision import block_movement
from config import Config
from entitybasic import Entity, register_entity
from geometry import Direction, Vec
from util import Util


class Dialogue:
    """Class to track an entity's dialogue."""

    def __init__(self, dialogue, conv_progress=None):
        """Initialize a Dialogue tracker."""
        self.dialogue = dialogue
        self.conv_progress = conv_progress or {}

    @staticmethod
    def from_json(dialogue_list):
        """Convert from JSON to a Dialogue object."""
        try:
            return Dialogue([
                {int(k): v for k, v in d.items()}
                if isinstance(d, dict) else d
                for d in dialogue_list])
        except ValueError:
            return None

    async def send_line(self, ws, entity_name, line):
        """Send a line of dialogue, which can be a string or list."""
        if isinstance(line, list):
            await Util.send_dialogue_choices(ws, entity_name, line)
        elif isinstance(line, str):
            await Util.send_dialogue(ws, entity_name, line)
        else:
            raise ValueError

    async def on_interact(self, event_ctx, entity):
        """Send dialogue when player interacts with the entity."""
        if event_ctx.username in self.conv_progress:
            self.conv_progress[event_ctx.username] += 1
            try:
                await self.send_line(
                    event_ctx.ws,
                    entity.name,
                    self.dialogue[self.conv_progress[event_ctx.username]])
                event_ctx.player.talking_to = entity
            except IndexError:
                del self.conv_progress[event_ctx.username]
                await self.end_dialogue(event_ctx, entity)
                event_ctx.player.talking_to = None
            except ValueError:
                del self.conv_progress[event_ctx.username]
                await self.on_interact(event_ctx, entity.name)
        else:
            self.conv_progress[event_ctx.username] = 0
            await self.send_line(
                event_ctx.ws,
                entity.name,
                self.dialogue[self.conv_progress[event_ctx.username]])
            event_ctx.player.talking_to = entity

    async def on_dialogue_choose(self, event_ctx, entity, choice):
        """Respond to player choosing dialogue."""
        if event_ctx.username in self.conv_progress:
            self.conv_progress[event_ctx.username] += 1
            try:
                await self.send_line(
                    event_ctx.ws,
                    entity.name,
                    self.dialogue[self.conv_progress[event_ctx.username]].get(
                        choice))
                event_ctx.player.talking_to = entity
            except IndexError:
                del self.conv_progress[event_ctx.username]
                await self.end_dialogue(event_ctx, entity)
                event_ctx.player.talking_to = None
            except ValueError:
                self.conv_progress[event_ctx.username] -= 1

    async def end_dialogue(self, event_ctx, entity):
        """End dialogue and call any handlers."""
        await Util.send_dialogue_end(event_ctx.ws, entity.name)
        try:
            await entity.on_dialogue_end(event_ctx)
        except AttributeError:
            pass


@register_entity("walker")
class Walker(Entity):
    """A basic Entity that walks and has dialogue.

    It walks three blocks to left and three blocks to the right.
    """

    def __init__(self, pos, velocity, facing, name, dialogue):
        """Initialize the Walker with certain default properties.

        Set velocity rightward with the norm of the given velocity.
        Set dialogue.
        Set min_x and max_x to three blocks left and three blocks to the right.
        """
        super().__init__(pos, velocity, facing, name)
        self.speed = self.velocity.norm()
        self.velocity = Vec(self.speed, 0)
        self.min_x = self.pos.x - Config.BLOCK_WIDTH*3
        self.max_x = self.pos.x + Config.BLOCK_WIDTH*3
        self.dialogue = dialogue

    def update(self, update_ctx):
        """Move and turn if min_x or max_x reached. Check for collision."""
        start_pos = self.pos
        super().update(update_ctx)
        if self.pos.x > self.max_x:
            self.facing = Direction.LEFT
            self.set_x(self.max_x - (self.pos.x - self.max_x))
            self.velocity = Vec(-self.speed, 0)
        elif self.pos.x < self.min_x:
            self.facing = Direction.RIGHT
            self.set_x(self.min_x + (self.min_x - self.pos.x))
            self.velocity = Vec(self.speed, 0)

        wall_entities = [
            entity for entity in update_ctx.world.entities
            if entity.blocks_movement
            and self.is_touching(entity)]
        wall_players = [
            player for player in
            update_ctx.game.get_players_by_world(
                update_ctx.world.get_world_id())
            if self.is_touching(player)]
        walls = wall_entities + wall_players
        if walls:
            walls.sort(
                key=lambda wall:
                wall.pos.dist_to(self.pos))
            for wall in walls:
                block_movement(wall.get_bounding_box(),
                               start_pos, self)

    async def on_interact(self, event_ctx):
        """Send dialogue when player interacts with Walker."""
        self.velocity = Vec(0, 0)
        await self.dialogue.on_interact(event_ctx, self)

    async def on_dialogue_choose(self, event_ctx, choice):
        """Respond to player choosing dialogue."""
        await self.dialogue.on_dialogue_choose(event_ctx, self, choice)

    async def on_dialogue_end(self, event_ctx):
        """Resume walking when dialogue ends."""
        del event_ctx  # Unused
        if self.facing is Direction.LEFT:
            self.velocity = Vec(-self.speed, 0)
        elif self.facing is Direction.RIGHT:
            self.velocity = Vec(self.speed, 0)

    def get_bounding_box(self):
        """Walker's bounding box is same as player's."""
        return super().get_bounding_box_of_width(Config.PLAYER_WIDTH)

    @staticmethod
    def from_json(entity_dict):
        """Convert a dict representing a JSON object into a Walker."""
        pos = Vec.from_json(entity_dict["pos"])
        velocity = Vec.from_json(entity_dict["velocity"])
        facing = Direction.str_to_direction(entity_dict["facing"])
        name = entity_dict["name"]
        dialogue = Dialogue.from_json(entity_dict["dialogue"])
        return Walker(pos, velocity, facing, name, dialogue)


@register_entity("stander")
class Stander(Entity):
    """A basic Entity that has dialogue and player interaction.

    It asks a question, lets the player respond yes or no, and then
    gives an answer based on the player's response.
    """

    def __init__(self, pos, velocity, facing, name, dialogue):
        """Initialize the Stander with certain default properties.

        Set velocity to 0.
        Set dialogue.
        """
        super().__init__(pos, velocity, facing, name)
        self.velocity = Vec(0, 0)
        self.dialogue = dialogue

    async def on_interact(self, event_ctx):
        """Send dialogue when player interacts with Stander."""
        await self.dialogue.on_interact(event_ctx, self)

    async def on_dialogue_choose(self, event_ctx, choice):
        """Respond to player choosing dialogue."""
        await self.dialogue.on_dialogue_choose(event_ctx, self, choice)

    def get_bounding_box(self):
        """Stander's bounding box is same as player's."""
        return super().get_bounding_box_of_width(Config.PLAYER_WIDTH)

    @staticmethod
    def from_json(entity_dict):
        """Convert a dict representing a JSON object into a Stander."""
        pos = Vec.from_json(entity_dict["pos"])
        velocity = Vec.from_json(entity_dict["velocity"])
        facing = Direction.str_to_direction(entity_dict["facing"])
        name = entity_dict["name"]
        dialogue = Dialogue.from_json(entity_dict["dialogue"])
        return Stander(pos, velocity, facing, name, dialogue)
