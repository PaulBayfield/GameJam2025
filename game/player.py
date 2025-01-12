from .dataclasses.player import PlayerData
import pygame

class Player(PlayerData, pygame.sprite.Sprite):
    def __init__(self, game, name: str) -> None:
        PlayerData.__init__(self, name)
        pygame.sprite.Sprite.__init__(self)

        self.x = 0
        self.y = 0
        self.direction = "down"
        self.game = game

        self.health = 100
        self.stamina = 100
        self.speed = 5

        self.sprites = {
            "up": self.load_sprites("up"),
            "down": self.load_sprites("down"),
            "left": self.load_sprites("left"),
            "right": self.load_sprites("right"),
        }
        self.current_sprite = 0
        self.image = self.sprites[self.direction][self.current_sprite]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def load_sprites(self, direction: str) -> list[pygame.Surface]:
        """Charge les sprites pour une direction donnée."""
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
        if self.direction == "up":
            self.y -= self.speed
            self.y = max(0, self.y)
        elif self.direction == "down":
            self.y += self.speed
            self.y = min(
                self.game.settings.WINDOW_HEIGHT - self.image.get_height(), self.y
            )
        elif self.direction == "left":
            self.x -= self.speed
            self.x = max(0, self.x)
        elif self.direction == "right":
            self.x += self.speed
            self.x = min(
                self.game.settings.WINDOW_WIDTH - self.image.get_width(), self.x
            )

        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites[self.direction]):
            self.current_sprite = 0
        self.image = self.sprites[self.direction][int(self.current_sprite)]

        self.rect.topleft = (self.x, self.y)


    def attack(self):
        print(f"{self.name} is attacking")


    def heal(self):
        print(f"{self.name} is healing")


    def dash(self):
        print(f"{self.name} is dashing")


    def draw(self, screen: pygame.Surface) -> None:
        """
        Efface la position précédente et dessine le joueur.
        :param screen: L'écran du jeu
        :type screen: pygame.Surface
        """
        # screen.fill((0, 0, 0), self.rect)  # Efface la trace
        screen.blit(self.image, (self.x, self.y))
