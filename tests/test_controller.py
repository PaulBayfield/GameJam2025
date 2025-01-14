import pytest
import pygame

from unittest.mock import Mock
from game.enums.game import GameState
from game.controller import Controller
from game.enums.keyboard import KeyboardType


class TestController:
    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Crée un objet Mock pour simuler le comportement de la classe Game
        et une instance de Controller.
        """
        self.mock_game = Mock()
        self.mock_game.running = True
        self.mock_game.state = GameState.PLAYING
        self.mock_game.settings.KEYBOARD_TYPE = KeyboardType.ZQSD
        self.mock_game.movement.handle = Mock()
        self.mock_game.movement.dash = Mock()
        self.controller = Controller(self.mock_game)

    def test_quit_event(self):
        """
        Teste que l'événement QUIT arrête le jeu.
        """
        event = pygame.event.Event(pygame.QUIT)
        self.controller.event(event)
        assert self.mock_game.running is False

    def test_arrow_keys(self):
        """
        Teste que les touches fléchées sont gérées correctement.
        """
        for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            event = pygame.event.Event(pygame.KEYDOWN, key=key)
            self.controller.event(event)
            self.mock_game.movement.handle.assert_called_with(key)

    def test_zqsd_keys(self):
        """
        Teste que les touches ZQSD sont gérées correctement.
        """
        for key in [pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s]:
            event = pygame.event.Event(pygame.KEYDOWN, key=key)
            self.controller.event(event)
            self.mock_game.movement.handle.assert_called_with(key)

    def test_wasd_keys(self):
        """
        Teste que les touches WASD sont gérées correctement.
        """
        self.mock_game.settings.KEYBOARD_TYPE = KeyboardType.WASD
        for key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
            event = pygame.event.Event(pygame.KEYDOWN, key=key)
            self.controller.event(event)
            self.mock_game.movement.handle.assert_called_with(key)

    def test_space_key(self):
        """
        Teste que la touche ESPACE déclenche le dash.
        """
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.controller.event(event)
        self.mock_game.movement.dash.assert_called_once()
