import pygame
import numpy as np
from .core import generate_perlin_noise_2d

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
        np.random.seed(0)
        noise = generate_perlin_noise_2d(
            (
                self.game.settings.WINDOW_HEIGHT
                // self.game.settings.TILE_SIZE,
                self.game.settings.WINDOW_WIDTH
                // self.game.settings.TILE_SIZE,
            ),
            (2, 2),
        )

        self.map = []
        for y in range(noise.shape[0]):
            row = []
            for x in range(noise.shape[1]):
                value = noise[y, x]
                if value < -0.1:
                    row.append(Tiles.GRASS)
                elif value < 0.5:
                    row.append(Tiles.GRASS_MEDIUM)
                else:
                    row.append(Tiles.GRASS_LARGE)
            self.map.append(row)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Fonction pour dessiner la carte du jeu

        :param screen: L'écran du jeu
        :type screen: pygame.Surface
        """
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if "image" in tile.value.keys():
                    image = pygame.image.load(tile.value["image"])
                    image = pygame.transform.scale(
                        image,
                        (
                            self.game.settings.TILE_SIZE,
                            self.game.settings.TILE_SIZE,
                        ),
                    )
                    surface.blit(
                        image,
                        (
                            x * self.game.settings.TILE_SIZE,
                            y * self.game.settings.TILE_SIZE,
                        ),
                    )
                else:
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
