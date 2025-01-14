import pygame
from typing import Dict, List, TYPE_CHECKING
from .dataclasses.player import PlayerData
from .enums.direction import Direction

if TYPE_CHECKING:
    from game.game import Game


class Player(PlayerData, pygame.sprite.Sprite):
    """
    Classe pour gérer les données et les animations du joueur
    """

    # Constantes de la classe
    SPRITE_FRAMES = 4
    DASH_COST = 40
    DASH_MULTIPLIER = 5
    MAX_HEALTH = 100
    MAX_STAMINA = 100
    BORDER_DAMAGE = 10
    BORDER_DASH_DAMAGE = 100

    def __init__(self, game: "Game", name: str) -> None:
        """
        Initialise le joueur avec un nom et les données de jeu
        :param game: Le jeu
        :type game: Game
        :param name: Le nom du joueur
        :type name: str
        """
        PlayerData.__init__(self, name)
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.position = pygame.math.Vector2(0, 0)  # Using Vector2 for position
        self.direction = Direction.DOWN
        self.damage_timestamp = pygame.time.get_ticks()

        # Charge et cache toutes les animations de sprites
        self.sprites = self._load_all_sprites()
        self.current_sprite_index = 0.0
        self.image = self.sprites[self.direction][0]
        self.rect = self.image.get_rect(topleft=self.position)

    def _load_all_sprites(self) -> Dict[Direction, List[pygame.Surface]]:
        """
        Charge toutes les animations de sprites pour chaque direction
        :return: Un dictionnaire de listes de surfaces pygame
        :rtype: Dict[Direction, List[pygame.Surface]]
        """
        return {
            direction: [
                pygame.image.load(
                    f"assets/sprites/hen/{direction.name.lower()}_{i}.png"
                ).convert_alpha()
                for i in range(1, self.SPRITE_FRAMES + 1)
            ]
            for direction in Direction
        }

    def _update_animation(self, speed: float = 0.1) -> None:
        """
        Met à jour l'animation du joueur en fonction de la direction actuelle
        :param speed: La vitesse de l'animation
        :type speed: float
        """
        self.current_sprite_index = (self.current_sprite_index + speed) % len(
            self.sprites[self.direction]
        )
        self.image = self.sprites[self.direction][
            int(self.current_sprite_index)
        ]

    def _check_bounds(self, new_pos: pygame.math.Vector2) -> bool:
        """
        Vérifie si la nouvelle position est dans les limites de l'écran
        :param new_pos: La nouvelle position du joueur
        :type new_pos: pygame.math.Vector2
        :return: True si la position est valide, False sinon
        :rtype: bool
        """
        return (
            0
            <= new_pos.x
            <= self.game.settings.WINDOW_WIDTH - self.image.get_width()
            and 0
            <= new_pos.y
            <= self.game.settings.WINDOW_HEIGHT - self.image.get_height()
        )

    def _handle_boundary_collision(self, damage_amount: int) -> None:
        """
        Gère les collisions avec les bords de l'écran
        :param damage_amount: Le montant de dégâts à infliger
        :type damage_amount: int
        """
        self.damage(damage_amount)
        self.position.x = max(
            0,
            min(
                self.position.x,
                self.game.settings.WINDOW_WIDTH - self.image.get_width(),
            ),
        )
        self.position.y = max(
            0,
            min(
                self.position.y,
                self.game.settings.WINDOW_HEIGHT - self.image.get_height(),
            ),
        )

    def change_direction(self, new_direction: Direction) -> None:
        """
        Change la direction du joueur et réinitialise l'animation
        :param new_direction: La nouvelle direction du joueur
        :type new_direction: Direction
        """
        if new_direction != self.direction:
            self.direction = new_direction
            self.current_sprite_index = 0

    def move(self) -> None:
        """
        Déplace le joueur dans la direction actuelle
        et gère les collisions avec les bords de l'écran
        """
        movement = pygame.math.Vector2()

        if self.direction == Direction.UP:
            movement.y = -self.speed
        elif self.direction == Direction.DOWN:
            movement.y = self.speed
        elif self.direction == Direction.LEFT:
            movement.x = -self.speed
        elif self.direction == Direction.RIGHT:
            movement.x = self.speed

        new_pos = self.position + movement

        if not self._check_bounds(new_pos):
            self._handle_boundary_collision(self.BORDER_DAMAGE)
        else:
            self.position = new_pos

        self._update_animation()
        self.rect.topleft = self.position

    def damage(self, amount: int) -> None:
        """
        Applique des dégâts au joueur et met à jour le timestamp des dégâts
        :param amount: Le montant de dégâts à infliger
        :type amount: int
        """
        self.health = max(0, self.health - amount)
        self.damage_timestamp = pygame.time.get_ticks() / self.health_regen

    def heal(self) -> None:
        """
        Régénère la santé du joueur au fil du temps
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.damage_timestamp >= 1000:
            self.health = min(self.MAX_HEALTH, self.health + 1)
            self.damage_timestamp = current_time

    def dash(self, direction: Direction) -> None:
        """
        Effectue un dash dans la direction spécifiée
        :param direction: La direction du dash
        :type direction: Direction
        """
        if self.stamina < self.DASH_COST:
            return

        self.stamina -= self.DASH_COST
        movement = pygame.math.Vector2()

        if direction == Direction.UP:
            movement.y = -self.speed * self.DASH_MULTIPLIER
        elif direction == Direction.DOWN:
            movement.y = self.speed * self.DASH_MULTIPLIER
        elif direction == Direction.LEFT:
            movement.x = -self.speed * self.DASH_MULTIPLIER
        elif direction == Direction.RIGHT:
            movement.x = self.speed * self.DASH_MULTIPLIER

        new_pos = self.position + movement

        if not self._check_bounds(new_pos):
            self._handle_boundary_collision(self.BORDER_DASH_DAMAGE)
        else:
            self.position = new_pos

        self._update_animation(0.1)
        self.rect.topleft = self.position

    def stamina_regen(self) -> None:
        """
        Régénère la stamina du joueur au fil du temps
        """
        self.stamina = min(self.MAX_STAMINA, self.stamina + 1)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine le joueur sur l'écran
        :param screen: La surface de l'écran
        :type screen: pygame.Surface
        """
        screen.blit(self.image, self.position)
