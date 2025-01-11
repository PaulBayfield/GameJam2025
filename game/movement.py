import pygame

from .enums.keyboard import KeyboardType
from .enums.direction import Direction
from typing import TYPE_CHECKING, Literal


if TYPE_CHECKING:
    from game.game import Game


class Movement:
    """
    Classe pour gérer les mouvements du joueur
    """

    def __init__(self, game: "Game") -> None:
        """
        Constructeur de la classe

        :param game: Le jeu
        :type game: Game
        """
        self.game = game

        self.key_mappings = {
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
        }

        self.zqsd_mappings = {
            pygame.K_q: Direction.LEFT,
            pygame.K_d: Direction.RIGHT,
            pygame.K_z: Direction.UP,
            pygame.K_s: Direction.DOWN,
        }

        self.wasd_mappings = {
            pygame.K_a: Direction.LEFT,
            pygame.K_d: Direction.RIGHT,
            pygame.K_w: Direction.UP,
            pygame.K_s: Direction.DOWN,
        }

    def handle(
        self,
        key: Literal[
            "pygame.K_LEFT",
            "pygame.K_RIGHT",
            "pygame.K_UP",
            "pygame.K_DOWN",
            "pygame.K_q",
            "pygame.K_d",
            "pygame.K_z",
            "pygame.K_s",
            "pygame.K_a",
            "pygame.K_w",
        ],
    ) -> None:
        """
        Fonction pour gérer les mouvements du joueur

        :param key: La touche du clavier
        :type key: Literal["pygame.K_LEFT", "pygame.K_RIGHT", "pygame.K_UP",
                                 "pygame.K_DOWN", "pygame.K_q", "pygame.K_d",
                                 "pygame.K_z", "pygame.K_s", "pygame.K_a",
                                 "pygame.K_w"
                              ]
        """
        # Vérifie les touches fléchées
        if key in self.key_mappings:
            print(self.key_mappings[key])

        # Vérifie les touches ZQSD ou WASD
        if (
            self.game.settings.KEYBOARD_TYPE == KeyboardType.ZQSD
            and key in self.zqsd_mappings
        ):
            print(self.zqsd_mappings[key])
        elif (
            self.game.settings.KEYBOARD_TYPE == KeyboardType.WASD
            and key in self.wasd_mappings
        ):
            print(self.wasd_mappings[key])

    def move(self, direction: Direction) -> None:
        """
        Fonction pour déplacer le joueur
        """
        if direction == Direction.UP:
            print("UP")
        elif direction == Direction.DOWN:
            print("DOWN")
        elif direction == Direction.LEFT:
            print("LEFT")
        elif direction == Direction.RIGHT:
            print("RIGHT")
