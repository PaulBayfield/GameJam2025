from .enemy import Enemy


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
