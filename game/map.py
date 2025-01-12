import pygame
import random

from .enums.tiles import Tiles
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.game import Game


class Map:
    """
    Classe pour gérer la carte du jeu
    """

    def __init__(self, game: "Game") -> None:
        """
        Constructeur de la classe

        :param game: Le jeu
        :type game: Game
        """
        self.game = game

        self.generate()

    def generate(self) -> None:
        """
        Fonction pour générer une carte aléatoire
        """
        self.map = [
            [
                random.choice(list(Tiles))
                for _ in range(self.game.settings.WINDOW_WIDTH)
            ]
            for _ in range(self.game.settings.WINDOW_HEIGHT)
        ]

    def draw(self, surface: pygame.Surface) -> None:
        """
        Fonction pour dessiner la carte du jeu

        :param screen: L'écran du jeu
        :type screen: pygame.Surface
        """
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                color = tile.value["color"]
                pygame.draw.rect(
                    surface,
                    color,
                    (
                        x * self.game.settings.TILE_SIZE,
                        y * self.game.settings.TILE_SIZE,
                        self.game.settings.TILE_SIZE,
                        self.game.settings.TILE_SIZE,
                    ),
                )
