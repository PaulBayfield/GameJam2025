import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game


class Interface:
    """
    Classe pour gérer l'interface du jeu
    """

    HEALTH_BAR_SIZE = (300, 10)
    HEALTH_COLOR = (78, 253, 0)
    HEALTH_LOW_COLOR = (254, 0, 2)
    STAMINA_COLOR = (109, 117, 238)
    STAMINA_LOW_COLOR = (63, 72, 204)

    def __init__(self, game: "Game") -> None:
        """
        Constructeur de la classe

        :param game: Le jeu
        :type game: Game
        """
        self.game = game

        self.player_health = None
        self.player_stamina = None

        self.heart_image = pygame.transform.scale(
            pygame.image.load("assets/heart.png").convert_alpha(), (20, 20)
        )
        self.potion_image = pygame.transform.scale(
            pygame.image.load("assets/potion.png").convert_alpha(), (20, 20)
        )

    def draw(self) -> None:
        """
        Affichage de l'interface de santé et d'endurance
        """
        # Barre de santé
        health_percentage = self.game.player.health / 100
        health_bar_width = int(self.HEALTH_BAR_SIZE[0] * health_percentage)
        health_bar_pos = (
            self.game.settings.WINDOW_WIDTH // 2
            - self.HEALTH_BAR_SIZE[0] // 2,
            self.game.settings.WINDOW_HEIGHT - 40,
        )

        # Affichage de la barre de santé
        pygame.draw.rect(
            self.game.screen,
            self.HEALTH_LOW_COLOR,
            (*health_bar_pos, *self.HEALTH_BAR_SIZE),
            0,
            0,
            0,
            8,
            0,
            8,
        )

        pygame.draw.rect(
            self.game.screen,
            self.HEALTH_COLOR,
            (*health_bar_pos, health_bar_width, self.HEALTH_BAR_SIZE[1]),
            0,
            0,
            0,
            8,
            0,
            8,
        )

        # Affichage de l'icône de coeur
        heart_icon_pos = (
            health_bar_pos[0] - 30,
            health_bar_pos[1]
            - (self.heart_image.get_height() // 2)
            + (self.HEALTH_BAR_SIZE[1] // 2),
        )
        self.game.screen.blit(self.heart_image, heart_icon_pos)

        # Barre d'endurance
        stamina_percentage = self.game.player.stamina / 100
        stamina_bar_width = int(self.HEALTH_BAR_SIZE[0] * stamina_percentage)
        stamina_bar_pos = (
            self.game.settings.WINDOW_WIDTH // 2
            - self.HEALTH_BAR_SIZE[0] // 2,
            self.game.settings.WINDOW_HEIGHT - 20,
        )

        # Affichage de la barre d'endurance
        pygame.draw.rect(
            self.game.screen,
            self.STAMINA_LOW_COLOR,
            (*stamina_bar_pos, *self.HEALTH_BAR_SIZE),
            0,
            0,
            0,
            8,
            0,
            8,
        )

        pygame.draw.rect(
            self.game.screen,
            self.STAMINA_COLOR,
            (*stamina_bar_pos, stamina_bar_width, self.HEALTH_BAR_SIZE[1]),
            0,
            0,
            0,
            8,
            0,
            8,
        )

        # Affichage de l'icône de potion
        potion_icon_pos = (
            stamina_bar_pos[0] - 30,
            stamina_bar_pos[1]
            - (self.potion_image.get_height() // 2)
            + (self.HEALTH_BAR_SIZE[1] // 2),
        )
        self.game.screen.blit(self.potion_image, potion_icon_pos)

    def update(self) -> None:
        """
        Mise à jour de l'interface
        """
        if (
            self.game.player.health != self.player_health
            or self.game.player.stamina != self.player_stamina
        ):
            self.draw()

            self.player_health = self.game.player.health
            self.player_stamina = self.game.player.stamina
