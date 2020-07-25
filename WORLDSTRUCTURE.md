# World file structure

Worlds are stored as JSON. Two different formats are used.

## Format for saving to file (this is version 0.4.0):
```json
{
  "$schema": "http://json-schema.org/draft/2019-09/schema#",
  "type": "object",
  "definitions": {
    "vec2": {
      "type": "object",
      "properties": {
        "x": {"type": "number"},
        "y": {"type": "number"}
      },
      "required": ["x", "y"]
    },
    "direction": {
      "type": "string",
      "enum": ["r", "d", "l", "u"]
    },
    "tile": {
      "type": "object",
      "properties": {
        "tile_id": {
          "type": "string",
          "$comment": "Should be snake_case"
        },
        "tile_data": {
          "type": "object",
          "$comment": "Optionally, any data that the tile needs."
        }
      },
      "required": ["tile_id"]
    },
    "entity": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "entity_id": {
          "type": "string",
          "$comment": "Should be snake_case"
        },
        "pos": {"$ref": "#/definitions/vec2"},
        "velocity": {"$ref": "#/definitions/vec2"},
        "facing": {"$ref": "#/definitions/direction"}
      },
      "required": ["name", "entity_id", "pos", "velocity", "facing"]
    },
    "spawn_point": {
      "type": "object",
      "properties": {
        "block_x": {"type": "integer", "minimum": 0},
        "block_y": {"type": "integer", "minimum": 0}
      },
      "required": ["block_x", "block_y"]
    },
    "cutscene": {
      "type": "object",
      "oneOf": [
        {
          "scene_type": {"const": "wait"},
          "wait_duration": {
            "type": "number",
            "$comment": "Wait time in seconds."
          }
        },
        {
          "scene_type": {"const": "move"},
          "entity_name": {
            "type": "string",
            "$comment": "Name of the entity to be moved."
          },
          "move_destination": {
            "$ref": "#/definitions/vec2",
            "$comment": "The position to be moved to."
          },
          "move_duration": {
            "type": "number",
            "$comment": "Move time in seconds."
          }
        },
        {
          "scene_type": {"const": "dialogue"},
          "entity_name": {
            "type": "string",
            "$comment": "Name of the entity that is talking."
          },
          "dialogue": {"type": "string"}
        }
      ]
    },
    "patch": {
      "type": "array",
      "items": {"$ref": "#/definitions/encounter"}
    },
    "encounter": {
      "type": "object",
      "properties": {
        "species": {"type": ["string", "null"]},
        "min_level": {"type": "number"},
        "max_level": {"type": "number"},
        "moves": {"type": "array", "items": {"type": "string"}},
        "weight": {"type": "number"}
      },
      "required": ["species", "min_level", "max_level", "moves", "weight"]
    }
  },
  "properties": {
    "version": {
      "const": "0.4.0"
    },
    "tiles": {
      "type": "array",
      "$comment": "List of rows of tiles. Tiles run in the same order as words run on a page.",
      "items": {
        "type": "array",
        "items": {"$ref": "#/definitions/tile"}
      }
    },
    "entities": {
      "type": "array",
      "items": {"$ref": "#/definitions/entity"}
    },
    "spawn_points": {
      "type": "object",
      "$comment": "The property name should be the spawn point ID.",
      "minProperties": 1,
      "additionalProperties": {"$ref": "#/definitions/spawn_point"}
    },
    "cutscenes": {
      "type": "array",
      "items": {"$ref": "#/definitions/cutscene"}
    },
    "patches": {
      "type": "object",
      "$comment": "The property name should be the patch ID.",
      "additionalProperties": {"$ref": "#/definitions/patch"}
    }
  },
  "required": ["version", "tiles", "entities", "spawn_points", "cutscenes", "patches"]
}
```

## Format for transmission to client (this is version 0.3.0):
```json
{
  "$schema": "http://json-schema.org/draft/2019-09/schema#",
  "definitions": {
    "vec2": {
      "type": "object",
      "properties": {
        "x": {"type": "number"},
        "y": {"type": "number"}
      },
      "required": ["x", "y"]
    },
    "direction": {
      "type": "string",
      "enum": ["r", "d", "l", "u"]
    },
    "tile": {
      "type": "object",
      "properties": {
        "tile_id": {
          "type": "string",
          "$comment": "Should be snake_case"
        },
        "tile_data": {
          "type": "object",
          "$comment": "Note that the client's tile data is a subset of the full tile data."
        }
      },
      "required": ["tile_id"]
    },
    "entity": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "entity_id": {
          "type": "string",
          "$comment": "Should be snake_case"
        },
        "pos": {"$ref": "#/definitions/vec2"},
        "velocity": {"$ref": "#/definitions/vec2"},
        "facing": {"$ref": "#/definitions/direction"}
      },
      "required": ["name", "entity_id", "pos", "velocity", "facing"]
    },
    "cutscene": {
      "type": "object",
      "oneOf": [
        {
          "scene_type": {"const": "wait"},
          "wait_duration": {
            "type": "number",
            "$comment": "Wait time in seconds."
          }
        },
        {
          "scene_type": {"const": "move"},
          "entity_name": {
            "type": "string",
            "$comment": "Name of the entity to be moved."
          },
          "move_destination": {
            "$ref": "#/definitions/vec2",
            "$comment": "The position to be moved to."
          },
          "move_duration": {
            "type": "number",
            "$comment": "Move time in seconds."
          }
        },
        {
          "scene_type": {"const": "dialogue"},
          "entity_name": {
            "type": "string",
            "$comment": "Name of the entity that is talking."
          },
          "dialogue": {"type": "string"}
        }
      ]
    }
  },
  "type": "object",
  "properties": {
    "version": {
      "const": "0.3.0"
    },
    "tiles": {
      "type": "array",
      "$comment": "List of rows of tiles. Tiles run in the same order as words run on a page.",
      "items": {"$ref": "#/definitions/tile"}
    },
    "entities": {
      "type": "array",
      "items": {"$ref": "#/definitions/entity"}
    },
    "spawn_pos": {"$ref": "#/definitions/vec2"},
    "cutscenes": {
      "type": "array",
      "items": {"$ref": "#/definitions/cutscene"}
    }
  },
  "required": ["version", "tiles", "entities", "spawn_pos", "cutscenes"]
}
```
