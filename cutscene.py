"""Defines the Cutscene class and its subclasses."""

from typing import Any, Dict

from geometry import Vec

_cutscenes: Dict[str, Any] = {}  # Maps scene_types to Cutscene classes.


class Cutscene:
    """Class for representing a move in a cutscene."""

    def __init__(self, cutscene_dict):
        """Initialize with the type of cutscene."""
        self.scene_type = cutscene_dict["scene_type"]

    @staticmethod
    def from_json(cutscene_dict):
        """Convert a dict representing a JSON object into a cutscene."""
        cutscene_class = Cutscene.get_cutscene_by_scene_type(
            cutscene_dict["scene_type"])
        cutscene = cutscene_class(cutscene_dict)
        return cutscene

    def to_json(self, is_to_client):
        """Convert a cutscene to a dict which can be converted to a JSON string.

        Args:
            is_to_client: True to get the version of the cutscene sent
                to the client, False to get the version of the cutscene
                to save to file.
        """

    @staticmethod
    def get_cutscene_by_scene_type(scene_type):
        """Get the Cutscene class corresponding to a scene_type."""
        cutscene_class = _cutscenes.get(scene_type)
        if not cutscene_class:
            raise ValueError
        return cutscene_class

    def get_scene_type(self):
        """Get the scene_type of a Cutscene."""
        cutscene_class = type(self)
        try:
            return next(
                scene_type for scene_type, cls in _cutscenes.items()
                if cls == cutscene_class)
        except StopIteration:
            raise ValueError


def register_cutscene(scene_type):
    """Class decorator to register the scene_type with a Cutscene class."""
    def decorator(cutscene_class):
        if scene_type in _cutscenes:
            raise ValueError
        _cutscenes[scene_type] = cutscene_class
        return cutscene_class
    return decorator


@register_cutscene("wait")
class WaitScene(Cutscene):
    """Represents nothing happening."""

    def __init__(self, cutscene_dict):
        """Set scene type and wait duration."""
        super().__init__(cutscene_dict)
        self.wait_duration = cutscene_dict["wait_duration"]

    def to_json(self, is_to_client):
        """Convert a cutscene to a dict which can be converted to a JSON string.

        Args:
            is_to_client: True to get the version of the cutscene sent
                to the client, False to get the version of the cutscene
                to save to file.
        """
        del is_to_client  # Unused
        return {
            "scene_type": self.scene_type,
            "wait_duration": self.wait_duration
        }


@register_cutscene("move")
class MoveScene(Cutscene):
    """Represents an entity moving."""

    def __init__(self, cutscene_dict):
        """Set scene type and other properties."""
        super().__init__(cutscene_dict)
        self.uuid = cutscene_dict["uuid"]
        self.move_destination = Vec.from_json(
            cutscene_dict["move_destination"])
        self.move_duration = cutscene_dict["move_duration"]

    def to_json(self, is_to_client):
        """Convert a cutscene to a dict which can be converted to a JSON string.

        Args:
            is_to_client: True to get the version of the cutscene sent
                to the client, False to get the version of the cutscene
                to save to file.
        """
        del is_to_client  # Unused
        return {
            "scene_type": self.scene_type,
            "uuid": self.uuid,
            "move_destination": self.move_destination.to_json(),
            "move_duration": self.move_duration
        }


@register_cutscene("dialogue")
class DialogueScene(Cutscene):
    """Represents an entity speaking."""

    def __init__(self, cutscene_dict):
        """Set scene type and other properties."""
        super().__init__(cutscene_dict)
        self.uuid = cutscene_dict["uuid"]
        self.dialogue = cutscene_dict["dialogue"]

    def to_json(self, is_to_client):
        """Convert a cutscene to a dict which can be converted to a JSON string.

        Args:
            is_to_client: True to get the version of the cutscene sent
                to the client, False to get the version of the cutscene
                to save to file.
        """
        del is_to_client  # Unused
        return {
            "scene_type": self.scene_type,
            "uuid": self.uuid,
            "dialogue": self.dialogue
        }
