from game.enums.keyboard import KeyboardType


class Settings:
    """
    Ce fichier contient les paramètres du jeu
    """

    # =========================================================================
    # Paramètres de la fenêtre
    # =========================================================================
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 900
    FPS = 30

    # =========================================================================
    # Paramètres du clavier
    # =========================================================================
    KEYBOARD_TYPE = KeyboardType.ZQSD  # KeyboardType.WASD

    # =========================================================================
    # Paramètres des tuiles
    # =========================================================================
    TILE_SIZE = 25
