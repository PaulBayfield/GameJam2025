from game.enums.direction import Direction
from .enemy import Enemy
import random


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
        self.can_change_direction = False

    def variant(self):
        """
        Changer la direction aléatoirement
        """
        # Wait 3 seconds before changing direction
        if self.can_change_direction:
            self.can_change_direction = False
            self.direction = random.choice(list(Direction))
            self.current_sprite_index = 0
        else:
            self.can_change_direction = True
