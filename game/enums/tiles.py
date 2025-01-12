from enum import Enum


class Tiles(Enum):
    """
    Enumération pour les types de clavier
    """

    DIRT = {
        "id": 0,
        "color": (139, 69, 19),
        "walkable": True,
        "name": "dirt",
    }
    GRASS = {
        "id": 1,
        "color": (0, 255, 0),
        "walkable": True,
        "name": "grass",
    }
    WATER = {
        "id": 2,
        "color": (0, 0, 255),
        "walkable": False,
        "name": "water",
    }
    # WALL = {
    #     "id": 3,
    #     "color": (255, 255, 255),
    #     "walkable": False,
    #     "name": "wall",
    # }
    TREE = {
        "id": 4,
        "color": (0, 128, 0),
        "walkable": False,
        "name": "tree",
    }
    GRASS_SMALL = {
        "id": 5,
        "color": (0, 128, 0),
        "walkable": True,
        "name": "grass_small",
    }
    GRASS_MEDIUM = {
        "id": 6,
        "color": (0, 128, 0),
        "walkable": True,
        "name": "grass_medium",
    }
    GRASS_LARGE = {
        "id": 7,
        "color": (0, 128, 0),
        "walkable": True,
        "name": "grass_large",
    }
    GRASS_XLARGE = {
        "id": 8,
        "color": (0, 128, 0),
        "walkable": True,
        "name": "grass_xlarge",
    }
    GRAVEL = {
        "id": 9,
        "color": (128, 128, 128),
        "walkable": True,
        "name": "gravel",
    }
