from .enemy import Enemy


class Knight(Enemy):
    """
    Classe représentant un chevalier dans le jeu.
    """

    def __init__(self, game, x, y, speed, direction):
        """
        Initialise un chevalier.

        :param game: Instance du jeu.
        :param x: Position x de départ.
        :param y: Position y de départ.
        :param speed: Vitesse de déplacement.
        :param direction: Direction initiale (vecteur [dx, dy]).
        """
        super().__init__(game, x, y, speed, direction, "knight")
        self.damage = 20
