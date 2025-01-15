import pygame
import os

from ..enums.direction import Direction
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
        direction: Direction,
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
        """
        super().__init__()
        self.game = game
        self.sprites = self._load_all_sprites(sprite_url)
        self.direction = direction
        self.image = self.sprites[self.direction][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.current_sprite_index = 0.0

    def _load_all_sprites(
        self, sprite_url: str
    ) -> dict[Direction, list[pygame.Surface]]:
        """
        Charge toutes les animations de sprites pour chaque direction
        :return: Un dictionnaire de listes de surfaces pygame
        :rtype: dict[Direction, list[pygame.Surface]]
        """
        # get the max number of frames
        j = 1
        while os.path.exists(f"assets/sprites/{sprite_url}/right_{j}.png"):
            j += 1
        return {
            direction: [
                pygame.transform.scale(
                    pygame.image.load(
                        f"assets/sprites/{sprite_url}/{direction.name.lower()}_{i}.png"
                    ),
                    (
                        self.game.settings.TILE_SIZE * 2,
                        self.game.settings.TILE_SIZE * 2,
                    ),
                ).convert_alpha()
                for i in range(1, j)
            ]
            for direction in Direction
        }

    def _update_animation(self, speed: float = 0.1) -> None:
        """
        Met à jour l'animation de l'ennemi en fonction de la direction actuelle
        :param speed: La vitesse de l'animation
        :type speed: float
        """
        self.current_sprite_index = (self.current_sprite_index + speed) % len(
            self.sprites[self.direction]
        )
        self.image = self.sprites[self.direction][
            int(self.current_sprite_index)
        ]

    def update(self):
        """
        Met à jour la position de l'ennemi.
        """

        if self.direction == Direction.UP:
            self.rect.y -= self.speed
        elif self.direction == Direction.DOWN:
            self.rect.y += self.speed
        elif self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        elif self.direction == Direction.RIGHT:
            self.rect.x += self.speed

        self._update_animation()

        # si la méthode "variant" est définie, on l'appelle
        if hasattr(self, "variant"):
            self.variant()

        # Vérifie si l'ennemi est hors de l'écran
        if not self.game.screen.get_rect().colliderect(self.rect):
            self.kill()
