import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game


class Item:
    """
    gère les Items qui apparaissent aléatoirement
    """

    def __init__(self, game: "Game"):
        """
        Constructeur de la classe

        :param game: Le jeu
        :type game: Game
        """
        self.game = game
        self.item_image = pygame.transform.scale(
            pygame.image.load("assets/chalencon.png"), (20, 20)
        )
        self.item_spawn = False
