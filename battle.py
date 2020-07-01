"""Defines the Battle class for battles."""
from collections import namedtuple
from enum import Enum, unique
import math
import random
import uuid


@unique
class Element(Enum):
    """The different elements.

    Different elements have different effectivenesses on each other.
    """

    UNTYPED = "untyped", "Untyped"
    EARTH = "earth", "Earth"
    METAL = "metal", "Metal"
    WATER = "water", "Water"
    AIR = "air", "Air"
    FIRE = "fire", "Fire"
    LIGHTNING = "lightning", "Lightning"
    PLANT = "plant", "Plant"

    def __init__(self, element_id, display_name):
        """Initialize with a unique name and a display name."""
        self.id = element_id
        self.display_name = display_name


@unique
class MoveType(Enum):
    """The three types of moves.

    Physical moves use attack and defense stats while magical moves
    use magic attack and magic defense stats. Non-attacking moves use
    neither.
    """

    PHYSICAL = "physical", "Physical"
    MAGIC = "magic", "Magic"
    NON_ATTACKING = "non_attacking", "Non-attacking"

    def __init__(self, move_type_id, display_name):
        """Initialize with a unique name and a display name."""
        self.id = move_type_id
        self.display_name = display_name


class MoveEffect:
    """The secondary effect of a move."""

    def activate(self):
        """Apply the move effect to the ongoing battle."""


class MoveEffects:
    """Helper functions/constants to create a MoveEffect."""

    NO_EFFECT = MoveEffect()


_Move = namedtuple("_Move", [
    "id",
    "display_name",
    "element",
    "type",
    "stamina_draw",
    "power",
    "move_time",
    "accuracy",
    "effect",
    "description"
])


class Move(Enum):
    """A move that a human/terrekin can use in combat."""

    PUNCH = _Move(
        id="punch",
        display_name="Punch",
        element=Element.UNTYPED,
        type=MoveType.PHYSICAL,
        stamina_draw=1,
        power=1,
        move_time=2,
        accuracy=1,
        effect=MoveEffects.NO_EFFECT,
        description="Punch your target.")

    KICK = _Move(
        id="kick",
        display_name="Kick",
        element=Element.UNTYPED,
        type=MoveType.PHYSICAL,
        stamina_draw=2,
        power=2,
        move_time=2,
        accuracy=1,
        effect=MoveEffects.NO_EFFECT,
        description="Kick your target.")

    SOIL_SLAP = _Move(
        id="soil_slap",
        display_name="Soil Slap",
        element=Element.EARTH,
        type=MoveType.MAGIC,
        stamina_draw=2,
        power=2,
        move_time=2,
        accuracy=1,
        effect=MoveEffects.NO_EFFECT,
        description="Slap your enemy with a hand made of soil.")

    def __init__(self, move_id, display_name, element, move_type,
                 stamina_draw, power, move_time, accuracy,
                 effect, description):
        """Initialize a Move."""
        self.id = move_id
        self.display_name = display_name
        self.element = element
        self.type = move_type
        self.stamina_draw = stamina_draw
        self.power = power
        self.move_time = move_time
        self.accuracy = accuracy
        self.effect = effect
        self.description = description

    @staticmethod
    def get_by_id(move_id):
        """Get the Move corresponding to a given ID."""
        for move in list(Move):
            if move.id == move_id:
                return move
        raise ValueError

    def to_json(self):
        """Convert a Move to a dict which can be converted to a JSON string."""
        return {
            "name": self.display_name,
            "element": self.element.id,
            "type": self.type.id,
            "stamina_draw": self.stamina_draw,
            "power": self.power,
            "move_time": self.move_time,
            "accuracy": self.accuracy,
            "description": self.description
        }


MoveChoice = namedtuple("MoveChoice", [
    "move",
    "target"
])


Stats = namedtuple("Stats", [
    "hp",
    "attack",
    "defense",
    "mattack",
    "mdefense",
    "speed",
    "charisma",
    "dex",
    "stam"
])


@unique
class Species(Enum):
    """The different species that exist ingame."""

    HUMAN = "human", "Human", Stats(
        hp=20,
        attack=2,
        defense=2,
        mattack=2,
        mdefense=2,
        speed=2,
        charisma=2,
        dex=2,
        stam=50
    )
    SCARPFALL = "scarpfall", "Scarpfall", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )
    ORELICK = "orelick", "Orelick", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )
    POUFFLE = "pouffle", "Poufflé", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )
    LAVADOREY = "lavadorey", "Lavadorey", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )
    DONNERLO = "donnerlo", "Donnerlo", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )
    VINELETTE = "vinelette", "Vinelette", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )
    WHIRLYBIRD = "whirlybird", "Whirlybird", Stats(
        hp=10,
        attack=1,
        defense=1,
        mattack=1,
        mdefense=1,
        speed=1,
        charisma=1,
        dex=1,
        stam=50
    )

    def __init__(self, species_id, display_name, base_stats):
        """Initialize with a unique name and a display name."""
        self.id = species_id
        self.display_name = display_name
        self.base_stats = base_stats

    @staticmethod
    def get_by_id(species_id):
        """Get the Species corresponding to a given ID."""
        for species in list(Species):
            if species.id == species_id:
                return species
        raise ValueError


class Combatant:
    """The Combatant describes something that can be in a Battle.

    Examples of things that are Combatants are Players and AICombatants.
    """

    def __init__(self, species, level, moves, base_stats=None):
        """Set the Combatant's stats and moves."""
        self.species = species
        self.level = level
        self.base_stats = base_stats or species.base_stats
        self.stats = self.get_stats()
        self.max_hp = self.stats.hp
        self.moves = moves
        self.is_ai = False
        self.combatant_id = None

    def get_stats(self):
        """Calculate the Combatant's stats using base stats and level."""
        return self.base_stats

    def reset_stats(self):
        """Reset any changes to stats."""
        self.stats = self.get_stats()
        self.max_hp = self.stats.hp

    def take_damage(self, damage):
        """Decrease the Combatant's HP by a given amount."""
        self.stats = self.stats._replace(hp=self.stats.hp-damage)

    def use_stamina(self, stamina_draw):
        """Decrease the Combatant's stamina by a given amount."""
        self.stats = self.stats._replace(stam=self.stats.stam-stamina_draw)


class AICombatant(Combatant):
    """The AICombatant is a Combatant whose strategy is computer-determined."""

    def __init__(self, species, level, moves, base_stats=None):
        """Set the Combatant's stats and moves and set is_AI to True."""
        super().__init__(species, level, moves, base_stats)
        self.is_ai = True

    def next_move(self, battle):
        """Given the current state of the battle, determine the next move.

        Returns:
            A MoveChoice.
        """


class RandomMoveAICombatant(AICombatant):
    """The RandomMoveAICombatant just chooses a random move every time."""

    def next_move(self, battle):
        """Just return a random move and target."""
        move = random.choice(self.moves)
        target = random.choice(list(c.combatant_id for c in battle.combatants
                                    if (c.combatant_id.side
                                        is not self.combatant_id.side)))
        return MoveChoice(move, target)


@unique
class Side(Enum):
    """Describes the two possible Sides of a battle."""

    SIDE_1 = "side1"
    SIDE_2 = "side2"


CombatantId = namedtuple("CombatantId", [
    "side",
    "combatant_uuid"
])


class Battle:
    """Describes a battle between a player and an AI."""

    def __init__(self, combatants1, combatants2):
        """Assign CombatantIDs to each Combatant."""
        self.combatants = combatants1 + combatants2
        for combatant in combatants1:
            generated_uuid = uuid.uuid4()
            c_id = CombatantId(Side.SIDE_1, generated_uuid)
            combatant.combatant_id = c_id
        for combatant in combatants2:
            generated_uuid = uuid.uuid4()
            c_id = CombatantId(Side.SIDE_2, generated_uuid)
            combatant.combatant_id = c_id

    def get_combatant_id_by_uuid(self, c_uuid):
        """Get the CombatantID associated with the given Combatant UUID.

        Raises ValueError if the Combatant is not found.
        """
        try:
            return next(combatant.combatant_id
                        for combatant in self.combatants
                        if combatant.combatant_id.combatant_uuid == c_uuid)
        except StopIteration:
            raise ValueError

    def get_combatant_by_id(self, c_id):
        """Get the Combatant with the given CombatantID in the battle.

        Raises ValueError if the Combatant is not found.
        """
        try:
            return next(combatant
                        for combatant in self.combatants
                        if combatant.combatant_id == c_id)
        except StopIteration:
            raise ValueError
        except AttributeError:
            raise ValueError

    def has_combatant(self, c_id):
        """Check if the Combatant given is in the battle."""
        try:
            if self.get_combatant_by_id(c_id):
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def get_eff_speed(user, move):
        """Get the effective speed of a combatant's move.

        Args:
            user: The Combatant to be assessed.
            move: The Move the combatant is using.
        """
        return user.stats.speed - move.move_time

    @staticmethod
    def get_eff_acc(user, move, target):
        """Get the likelihood a move will hit, as a number between 0 and 1.

        Args:
            user: The Combatant using the move.
            move: The Move the combatant is using.
            target: The Combatant who is being hit by the move.
        """
        ratio = ((user.stats.dex - target.stats.dex)
                 / (user.stats.dex + target.stats.dex))
        multiplier = (0.4/(1+0.000912**ratio)) + 0.8
        return move.accuracy * multiplier

    @staticmethod
    def get_damage(level, attack, defense, power, multiplier):
        """Get the damage caused by a move.

        Args:
            level: The level of the attacker.
            attack: Either the attack or magic attack of the attacker,
                depending on the move used.
            defense: Either the defense or magic defense of the attacker,
                depending on the move used.
            power: The power of the move.
            multiplier: Any multiplier, due to elemental matchups
                or buffs.
        """
        return math.ceil(0.3*(1.002**level)*(attack*power/defense)*multiplier)

    def process_player_move(self, player_move):
        """Given the player move, process a turn. Return winner if any.

        Only valid if there is only one player-controlled Combatant.
        Returns:
            The winning battle Side. If there is no winner yet, None
            is returned.
        """
        return self.process_moves({
            combatant.combatant_id:
                combatant.next_move(self) if combatant.is_ai else player_move
            for combatant in self.combatants})

    def process_moves(self, moves):
        """Given the combatant moves, process a turn. Return winner if any.

        Args:
            moves: A dict with CombatantIds as keys and MoveChoices as values.
        Returns:
            The winning battle Side. If there is no winner yet, None
            is returned.
        """
        self.combatants.sort(key=lambda combatant:
                             Battle.get_eff_speed(
                                 combatant,
                                 moves[combatant.combatant_id].move),
                             reverse=True)
        for combatant in self.combatants:
            if not combatant:
                continue
            move_choice = moves[combatant.combatant_id]
            try:
                target = self.get_combatant_by_id(move_choice.target)
            except ValueError:
                continue
            move = move_choice.move
            if random.random() < Battle.get_eff_acc(combatant,
                                                    move,
                                                    target):
                self.process_move(combatant, target, move)
        self.combatants = [c for c in self.combatants if c]
        return self.get_winner()

    def process_move(self, attacker, defender, move):
        """Process one move.

        Args:
            attacker: The attacking Combatant.
            defender: The Combatant that is the target of the move.
            move: The Move.
        """
        if move.type is MoveType.PHYSICAL:
            defender.take_damage(
                Battle.get_damage(attacker.level,
                                  attacker.stats.attack,
                                  defender.stats.defense,
                                  move.power,
                                  1))
        elif move.type is MoveType.MAGIC:
            defender.take_damage(
                Battle.get_damage(attacker.level,
                                  attacker.stats.mattack,
                                  defender.stats.mdefense,
                                  move.power,
                                  1))
        self.check_for_kills()
        move.effect.activate()
        self.check_for_kills()
        if attacker:
            attacker.use_stamina(move.stamina_draw)
            self.check_for_kills()

    def check_for_kills(self):
        """Check if any combatants have HP or stamina <= 0 and remove them.

        Sets Combatants that have been killed to None so that they can be
        removed later.
        """
        for i, combatant in enumerate(self.combatants):
            if (combatant and
                    (combatant.stats.hp <= 0 or combatant.stats.stam <= 0)):
                self.combatants[i] = None

    def get_winner(self):
        """Return winning battle side based on Combatants left.

        Returns:
            The winning battle Side. If there is no winner yet, None
            is returned.
        """
        if all(combatant.combatant_id.side is Side.SIDE_1
               for combatant in self.combatants):
            return Side.SIDE_1
        if all(combatant.combatant_id.side is Side.SIDE_2
               for combatant in self.combatants):
            return Side.SIDE_2
        return None

    def to_json(self, client_side):
        """Convert a Battle to a dict which can be converted to a JSON string.

        Args:
            side: The Side to which the JSON string is going to be sent to.
                This is used to determine which pieces of information should
                be excluded from the return value.
        """
        obj = {}
        for side in [Side.SIDE_1, Side.SIDE_2]:
            side_obj = {}
            side_combatants = [combatant
                               for combatant in self.combatants
                               if combatant.combatant_id.side is side]
            for combatant in side_combatants:
                if side is client_side:
                    combatant_obj = {
                        "species": combatant.species.id,
                        "level": combatant.level,
                        "stats": combatant.stats._asdict(),
                        "max_hp": combatant.max_hp,
                        "moves": [m.to_json() for m in combatant.moves]
                    }
                else:
                    combatant_obj = {
                        "species": combatant.species.id,
                        "level": combatant.level,
                        "hp_proportion": combatant.stats.hp/combatant.max_hp
                    }
                combatant_uuid = combatant.combatant_id.combatant_uuid
                side_obj[combatant_uuid.hex] = combatant_obj
            obj[side.value] = side_obj
        return obj
