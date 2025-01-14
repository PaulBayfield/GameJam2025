import pygame
import random
from game.enemies.knight import Knight


class EnemySpawner:
    """
    Classe pour gérer la génération d'ennemis en vagues.
    """

    def __init__(self, game, wave_interval=3000, max_enemies_per_wave=10):
        """
        Initialise le générateur d'ennemis.
        :param game: Instance du jeu.
        :param wave_interval: Temps entre les vagues (en ms).
        :param max_enemies_per_wave: Nombre maximum d'ennemis par vague.
        """
        self.game = game
        self.wave_interval = wave_interval
        self.max_enemies_per_wave = max_enemies_per_wave
        self.last_wave_time = pygame.time.get_ticks()
        self.enemies = pygame.sprite.Group()

    def spawn_wave(self):
        """
        Génère une vague d'ennemis.
        """
        for _ in range(random.randint(1, self.max_enemies_per_wave)):
            # Détermine un bord aléatoire pour faire apparaître l'ennemi
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(1, self.game.settings.WINDOW_WIDTH - 1)
                y = 0
                direction = (0, 1)
            elif side == "bottom":
                x = random.randint(1, self.game.settings.WINDOW_WIDTH - 1)
                y = self.game.settings.WINDOW_HEIGHT
                direction = (0, -1)
            elif side == "left":
                x = 0
                y = random.randint(1, self.game.settings.WINDOW_HEIGHT - 1)
                direction = (1, 0)
            elif side == "right":
                x = self.game.settings.WINDOW_WIDTH
                y = random.randint(1, self.game.settings.WINDOW_HEIGHT - 1)
                direction = (-1, 0)

            speed = random.uniform(1, 3)
            if random.random() < 0.5:
                enemy = Knight(self.game, x, y, speed, direction)
            else:
                enemy = Knight(self.game, x, y, speed, direction)
            self.enemies.add(enemy)

    def update(self):
        """
        Met à jour les ennemis et gère les vagues.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_wave_time >= self.wave_interval:
            self.spawn_wave()
            self.last_wave_time = current_time

        self.enemies.update()

    def draw(self, surface):
        """
        Dessine tous les ennemis.
        :param surface: Surface sur laquelle dessiner.
        """
        self.enemies.draw(surface)
