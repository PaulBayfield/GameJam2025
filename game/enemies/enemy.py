import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game


class Enemy(pygame.sprite.Sprite):
    """
    Classe représentant un ennemi dans le jeu.
    """

    def __init__(
        self,
        game: "Game",
        x: int,
        y: int,
        speed: int,
        direction: list[int, int],
        sprite_url: str = "enemy",
    ):
        """
        Initialise un ennemi.

        :param game: Instance du jeu.
        :type game: Game
        :param x: Position x de départ.
        :type x: int
        :param y: Position y de départ.
        :type y: int
        :param speed: Vitesse de déplacement.
        :type speed: int
        :param direction: Direction initiale (vecteur [dx, dy]).
        :type direction: list[int, int]
        """
        super().__init__()
        self.game = game
        self.image = pygame.image.load(
            f"assets/sprites/{sprite_url}/right_1.png"
        ).convert_alpha()
        # self.image = pygame.transform.scale(
        #     self.image, (game.settings.TILE_SIZE, game.settings.TILE_SIZE)
        # )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = pygame.Vector2(direction)

    def update(self):
        """
        Met à jour la position de l'ennemi.
        """
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Vérifie si l'ennemi est hors de l'écran
        if not self.game.screen.get_rect().colliderect(self.rect):
            self.kill()
