from enum import Enum


class Tiles(Enum):
    """
    Énumération pour les types de clavier
    """

    # DIRT = {
    #     "id": 0,
    #     "color": (139, 69, 19),
    #     "walkable": True,
    #     "name": "dirt",
    # }
    GRASS = {
        "id": 1,
        "image": "assets/images/map/grass.jpg",
        "walkable": True,
        "name": "grass",
    }
    # WATER = {
    #     "id": 2,
    #     "color": (0, 0, 255),
    #     "walkable": False,
    #     "name": "water",
    # }
    # WALL = {
    #     "id": 3,
    #     "color": (255, 255, 255),
    #     "walkable": False,
    #     "name": "wall",
    # }
    # TREE = {
    #     "id": 4,
    #     "color": (0, 128, 0),
    #     "walkable": False,
    #     "name": "tree",
    # }
    GRASS_SMALL = {
        "id": 2,
        "image": "assets/images/map/grass_medium_fower2.jpg",
        "walkable": True,
        "name": "grass_small",
    }
    GRASS_MEDIUM = {
        "id": 6,
        "image": "assets/images/map/grass_medium.jpg",
        "walkable": True,
        "name": "grass_medium",
    }
    GRASS_LARGE = {
        "id": 7,
        "image": "assets/images/map/grass_large.jpg",
        "walkable": True,
        "name": "grass_large",
    }
