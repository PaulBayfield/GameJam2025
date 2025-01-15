import pytest
import pygame

from unittest.mock import Mock, patch
from game.components.interface import Interface


class TestInterface:
    @pytest.fixture(scope="module", autouse=True)
    def pygame_setup_teardown(self):
        """
        Initialise et ferme Pygame avant et après les tests.
        """
        pygame.init()
        pygame.display.set_mode((1, 1))  # Crée une fenêtre factice
        yield
        pygame.quit()

    @pytest.fixture
    def mock_game(self):
        """
        Crée un objet Mock pour simuler le comportement de la classe Game.
        """
        game = Mock()
        game.player.health = 100
        game.player.stamina = 100
        game.settings.WINDOW_WIDTH = 800
        game.settings.WINDOW_HEIGHT = 600
        game.screen = pygame.Surface((800, 600))  # Utilise une vraie surface
        return game

    @pytest.fixture
    @patch("pygame.image.load")
    def interface(self, mock_load, mock_game):
        """
        Crée une instance de la classe Interface avec un mock de Game.
        """
        mock_image = pygame.Surface((20, 20))
        mock_load.return_value = mock_image
        return Interface(mock_game)

    def test_draw_health_bar(self, interface, mock_game):
        """
        Teste que la barre de santé est correctement dessinée.
        """
        mock_game.player.health = 50
        interface.draw()

        health_percentage = 0.5
        health_bar_width = int(
            Interface.HEALTH_BAR_SIZE[0] * health_percentage
        )
        health_bar_pos = (
            mock_game.settings.WINDOW_WIDTH // 2
            - Interface.HEALTH_BAR_SIZE[0] // 2,
            mock_game.settings.WINDOW_HEIGHT - 40,
        )

        # Vérifie qu'une partie de la barre de santé est dessinée
        pixel_array = pygame.PixelArray(mock_game.screen)
        assert any(
            pixel_array[x, health_bar_pos[1]]
            == mock_game.screen.map_rgb(Interface.HEALTH_COLOR)
            for x in range(
                health_bar_pos[0], health_bar_pos[0] + health_bar_width
            )
        )

    def test_draw_stamina_bar(self, interface, mock_game):
        """
        Teste que la barre d'endurance est correctement dessinée.
        """
        mock_game.player.stamina = 75
        interface.draw()

        stamina_percentage = 0.75
        stamina_bar_width = int(
            Interface.HEALTH_BAR_SIZE[0] * stamina_percentage
        )
        stamina_bar_pos = (
            mock_game.settings.WINDOW_WIDTH // 2
            - Interface.HEALTH_BAR_SIZE[0] // 2,
            mock_game.settings.WINDOW_HEIGHT - 20,
        )

        # Vérifie qu'une partie de la barre d'endurance est dessinée
        pixel_array = pygame.PixelArray(mock_game.screen)
        assert any(
            pixel_array[x, stamina_bar_pos[1]]
            == mock_game.screen.map_rgb(Interface.STAMINA_COLOR)
            for x in range(
                stamina_bar_pos[0], stamina_bar_pos[0] + stamina_bar_width
            )
        )

    def test_draw_icons(self, interface, mock_game):
        """
        Teste que les icônes de coeur et de potion sont correctement affichées.
        """
        interface.draw()

        health_bar_pos = (
            mock_game.settings.WINDOW_WIDTH // 2
            - Interface.HEALTH_BAR_SIZE[0] // 2,
            mock_game.settings.WINDOW_HEIGHT - 40,
        )
        heart_icon_pos = (
            health_bar_pos[0] - 30,
            health_bar_pos[1]
            - (interface.heart_image.get_height() // 2)
            + (Interface.HEALTH_BAR_SIZE[1] // 2),
        )

        stamina_bar_pos = (
            mock_game.settings.WINDOW_WIDTH // 2
            - Interface.HEALTH_BAR_SIZE[0] // 2,
            mock_game.settings.WINDOW_HEIGHT - 20,
        )
        potion_icon_pos = (
            stamina_bar_pos[0] - 30,
            stamina_bar_pos[1]
            - (interface.potion_image.get_height() // 2)
            + (Interface.HEALTH_BAR_SIZE[1] // 2),
        )

        # Vérifie que les icônes sont placées sur la surface
        assert mock_game.screen.get_at(
            heart_icon_pos
        ) != mock_game.screen.map_rgb((0, 0, 0))
        assert mock_game.screen.get_at(
            potion_icon_pos
        ) != mock_game.screen.map_rgb((0, 0, 0))

    def test_update(self, interface, mock_game):
        """
        Teste que la méthode update met correctement à jour l'interface.
        """
        mock_game.player.health = 90
        mock_game.player.stamina = 80

        interface.update()

        assert interface.player_health == 90
        assert interface.player_stamina == 80
