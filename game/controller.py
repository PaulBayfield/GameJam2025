import pygame

from pygame.event import Event
from .enums.game import GameState
from .enums.keyboard import KeyboardType
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.game import Game


class Controller:
    """
    Classe pour gérer les contrôles du jeu
    """

    def __init__(self, game: "Game") -> None:
        """
        Constructeur de la classe

        :param game: Le jeu
        :type game: Game
        """
        self.game = game

    def event(self, event: Event) -> None:
        """
        Fonction pour gérer les événements

        :param event: L'événement à gérer
        :type event: Event
        """
        if event.type == pygame.QUIT:
            self.game.running = False

        # Traite les touches du clavier
        if event.type == pygame.KEYDOWN:
            if self.game.state == GameState.PLAYING:
                # Traite les touches fléchées
                if event.key in [
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                ]:
                    self.game.movement.handle(event.key)

                # Traite les touches ZQSD
                if (
                    self.game.settings.KEYBOARD_TYPE == KeyboardType.ZQSD
                    and event.key
                    in [
                        pygame.K_q,
                        pygame.K_d,
                        pygame.K_z,
                        pygame.K_s,
                    ]
                ):
                    self.game.movement.handle(event.key)

                # Traite les touches WASD
                if (
                    self.game.settings.KEYBOARD_TYPE == KeyboardType.WASD
                    and event.key
                    in [
                        pygame.K_a,
                        pygame.K_d,
                        pygame.K_w,
                        pygame.K_s,
                    ]
                ):
                    self.game.movement.handle(event.key)

                # Traite la touche ESPACE
                if event.key == pygame.K_SPACE:
                    self.game.movement.dash()

            # Traite la touche P
            if event.key == pygame.K_p:
                if self.game.paused:
                    self.game.paused = False
                    self.game.state = GameState.PLAYING
                else:
                    self.game.state = GameState.PAUSED

            # Traite la touche ECHAP
            if event.key == pygame.K_ESCAPE:
                self.game.state = GameState.END
