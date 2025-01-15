import random

from ..enums.direction import Direction
from .enemy import Enemy
from time import time
from random import randint


class Pirate(Enemy):
    """
    Classe représentant un pirate dans le jeu.
    """

    def __init__(self, game, x, y, speed, direction):
        """
        Initialise un pirate.

        :param game: Instance du jeu.
        :param x: Position x de départ.
        :param y: Position y de départ.
        :param speed: Vitesse de déplacement.
        :param direction: Direction initiale (vecteur [dx, dy]).
        """
        super().__init__(game, x, y, speed, direction, "pirate")

        self.wait_time = randint(1, 5)
        self.last_direction_change = time()

    def variant(self):
        """
        Changer la direction aléatoirement
        """
        if time() - self.last_direction_change >= self.wait_time:
            self.direction = random.choice(list(Direction))
            self.last_direction_change = time()
            self.current_sprite_index = 0
