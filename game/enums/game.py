from enum import Enum, auto


class GameState(Enum):
    """
    Enumeration pour les états du jeu
    """

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    END = auto()
