import pygame

from .dataclasses.player import PlayerData
from .enums.direction import Direction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game


class Player(PlayerData, pygame.sprite.Sprite):
    """
    Classe pour gérer le joueur
    """

    def __init__(self, game: "Game", name: str) -> None:
        """
        Constructeur de la classe

        :param game: Le jeu
        :type game: Game
        :param name: Le nom du joueur
        :type name: str
        """
        PlayerData.__init__(self, name)
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.x = 0
        self.y = 0
        self.direction = Direction.DOWN
        self.damage_timestamp = pygame.time.get_ticks()

        self.sprites = {
            Direction.UP: self.load_sprites("up"),
            Direction.DOWN: self.load_sprites("down"),
            Direction.LEFT: self.load_sprites("left"),
            Direction.RIGHT: self.load_sprites("right"),
        }
        self.current_sprite = 0
        self.image = self.sprites[self.direction][self.current_sprite]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def load_sprites(self, direction: str) -> list[pygame.Surface]:
        """
        Charge les sprites pour une direction donnée.

        :param direction: La direction du joueur
        :type direction: str
        :return: La liste des sprites
        :rtype: list[pygame.Surface]
        """
        sprite_list = []
        for i in range(1, 5):  # Suppose 4 frames par animation
            sprite_path = f"assets/sprites/hen/{direction}_{i}.png"
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite_list.append(sprite)
        return sprite_list

    def change_direction(self, direction: str) -> None:
        """
        Change la direction du joueur

        :param direction: La direction du joueur
        :type direction: str
        """
        if direction != self.direction:
            self.direction = direction
            self.current_sprite = 0

    def move(self) -> None:
        """
        Déplace le joueur
        """
        if self.direction == Direction.UP:
            self.y -= self.speed

            if self.y < 0:
                self.damage(10)

            self.y = max(0, self.y)
        elif self.direction == Direction.DOWN:
            self.y += self.speed

            if (
                self.y
                > self.game.settings.WINDOW_HEIGHT - self.image.get_height()
            ):
                self.damage(10)

            self.y = min(
                self.game.settings.WINDOW_HEIGHT - self.image.get_height(),
                self.y,
            )
        elif self.direction == Direction.LEFT:
            self.x -= self.speed

            if self.x < 0:
                self.damage(10)

            self.x = max(0, self.x)
        elif self.direction == Direction.RIGHT:
            self.x += self.speed

            if (
                self.x
                > self.game.settings.WINDOW_WIDTH - self.image.get_width()
            ):
                self.damage(10)

            self.x = min(
                self.game.settings.WINDOW_WIDTH - self.image.get_width(),
                self.x,
            )

        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites[self.direction]):
            self.current_sprite = 0
        self.image = self.sprites[self.direction][int(self.current_sprite)]

        self.rect.topleft = (self.x, self.y)

    def damage(self, amount: int) -> None:
        """
        Inflige des dégâts au joueur

        :param amount: La quantité de dégâts
        :type amount: int
        """
        self.health -= amount
        self.damage_timestamp = pygame.time.get_ticks() / self.health_regen

        if self.health <= 0:
            self.health = 0

    def attack(self) -> None:
        print(f"{self.name} is attacking")

    def heal(self) -> None:
        """
        Soigne le joueur
        """
        if self.damage_timestamp + 1000 < pygame.time.get_ticks():
            self.health += 1

            if self.health > 100:
                self.health = 100

            self.damage_timestamp = pygame.time.get_ticks()

    def dash(self, direction: Direction) -> None:
        """
        Fait un dash

        :param direction: La direction du dash
        :type direction: Direction
        """
        if self.stamina >= 40:
            self.stamina -= 40

            if direction == Direction.UP:
                self.y -= self.speed * 5

                if self.y < 0:
                    self.damage(100)
            elif direction == Direction.DOWN:
                self.y += self.speed * 5

                if (
                    self.y
                    > self.game.settings.WINDOW_HEIGHT
                    - self.image.get_height()
                ):
                    self.damage(100)
            elif direction == Direction.LEFT:
                self.x -= self.speed * 5

                if self.x < 0:
                    self.damage(100)
            elif direction == Direction.RIGHT:
                self.x += self.speed * 5

                if (
                    self.x
                    > self.game.settings.WINDOW_WIDTH - self.image.get_width()
                ):
                    self.damage(100)

            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites[direction]):
                self.current_sprite = 0
            self.image = self.sprites[direction][int(self.current_sprite)]

    def stamina_regen(self) -> None:
        """
        Régénère l'endurance du joueur
        """
        if self.stamina < 100:
            self.stamina += 1

    def draw(self, screen: pygame.Surface) -> None:
        """
        Efface la position précédente et dessine le joueur.
        :param screen: L'écran du jeu
        :type screen: pygame.Surface
        """
        screen.blit(self.image, (self.x, self.y))
