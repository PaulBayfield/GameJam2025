import pygame
import random

from time import time
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
            pygame.image.load("assets/chalencon.png"),
            (self.game.settings.ITEM_SIZE, self.game.settings.ITEM_SIZE),
        )
        self.item_spawn = False
        self.item_effect = False
        self.rect = self.item_image.get_rect()

        self.timestamp = time()

    def spawn_item(self):
        """
        Fait apparaître l'item sur la carte
        """
        # Position aléatoire sur la carte
        self.rect.x = random.randint(
            0, self.game.settings.WINDOW_WIDTH - self.rect.width
        )
        self.rect.y = random.randint(
            0, self.game.settings.WINDOW_HEIGHT - self.rect.height
        )
        self.item_spawn = True

    def draw(self):
        """
        Dessine l'item sur l'écran si il est apparu
        """
        if not self.item_spawn:
            # Effectue un test aléatoire avec une faible probabilité
            if random.random() < 0.002:  # 1% de chance que l'item apparaisse
                self.spawn_item()

        self.check_item()
        if self.item_spawn:
            self.game.screen.blit(self.item_image, self.rect)

    def check_item(self):
        if self.rect.colliderect(self.game.player.rect) and self.item_spawn:
            self.timestamp = time() + 5
            self.item_spawn = False
            self.item_effect = True
            self.game.player.take_song.set_volume(0.3)
            self.game.player.take_song.play()
            self.game.player.onFire = True
        elif self.timestamp < time():
            self.item_effect = False
            self.game.player.onFire = False
