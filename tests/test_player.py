import pytest
import pygame
from unittest.mock import Mock, patch
from typing import Dict, List
from game.enums.direction import Direction
from game.player import Player


@pytest.fixture
def mock_game():
    """Fixture pour créer un mock du jeu"""
    game = Mock()
    game.settings.WINDOW_WIDTH = 800
    game.settings.WINDOW_HEIGHT = 600
    return game


@pytest.fixture
def mock_sprites() -> Dict[Direction, List[pygame.Surface]]:
    """Fixture pour créer des sprites mockés"""
    sprites = {}
    for direction in Direction:
        sprites[direction] = [pygame.Surface((32, 32)) for _ in range(4)]
    return sprites


@pytest.fixture
def player(mock_game, monkeypatch):
    """Fixture pour créer un joueur avec des dépendances mockées"""

    # Mock le chargement des sprites
    def mock_load_sprites(*args) -> Dict[Direction, List[pygame.Surface]]:
        return {
            direction: [pygame.Surface((32, 32)) for _ in range(4)]
            for direction in Direction
        }

    monkeypatch.setattr(Player, "_load_all_sprites", mock_load_sprites)

    return Player(mock_game, "TestPlayer")


class TestPlayer:
    """Tests pour la classe Player"""

    def test_player_initialization(self, player):
        """Teste l'initialisation correcte du joueur"""
        assert player.name == "TestPlayer"
        assert player.position == pygame.math.Vector2(0, 0)
        assert player.direction == Direction.DOWN
        assert player.health == 100
        assert player.stamina == 100
        assert isinstance(player.sprites[Direction.DOWN], list)
        assert len(player.sprites[Direction.DOWN]) == 4

    def test_change_direction(self, player):
        """Teste le changement de direction"""
        player.change_direction(Direction.UP)

        assert player.direction == Direction.UP
        assert player.current_sprite_index == 0

        # Test pas de changement si même direction
        player.current_sprite_index = 2.5
        player.change_direction(Direction.UP)
        assert player.current_sprite_index == 2.5

    def test_move_within_bounds(self, player):
        """Teste le mouvement dans les limites de l'écran"""
        initial_pos = pygame.math.Vector2(100, 100)
        player.position = initial_pos
        player.speed = 5

        # Test mouvement vers le haut
        player.direction = Direction.UP
        player.move()
        assert player.position.y == initial_pos.y - player.speed

        # Test mouvement vers la droite
        player.direction = Direction.RIGHT
        player.move()
        assert player.position.x == initial_pos.x + player.speed

    def test_move_out_of_bounds(self, player):
        """Teste le mouvement hors des limites de l'écran"""
        player.position = pygame.math.Vector2(-5, -5)
        initial_health = player.health

        player.move()

        assert player.position.x >= 0
        assert player.position.y >= 0
        assert player.health < initial_health

    def test_damage(self, player):
        """Teste l'application des dégâts"""
        initial_health = player.health
        damage_amount = 30

        player.damage(damage_amount)

        assert player.health == initial_health - damage_amount

    def test_heal(self, player):
        """Teste la régénération de santé"""
        player.health = 50
        initial_timestamp = player.damage_timestamp

        with patch(
            "pygame.time.get_ticks", return_value=initial_timestamp + 2000
        ):
            player.heal()
            assert player.health == 51

    def test_dash(self, player):
        """Teste le dash"""
        initial_pos = pygame.math.Vector2(100, 100)
        player.position = initial_pos
        player.speed = 5
        initial_stamina = player.stamina

        # Test dash avec assez de stamina
        player.dash(Direction.RIGHT)
        assert player.stamina == initial_stamina - player.DASH_COST
        assert player.position.x > initial_pos.x

        # Test dash sans assez de stamina
        player.stamina = 0
        initial_pos = player.position
        player.dash(Direction.RIGHT)
        assert player.position == initial_pos

    def test_stamina_regen(self, player):
        """Teste la régénération de stamina"""
        player.stamina = 50
        player.stamina_regen()
        assert player.stamina == 51

        # Test que la stamina ne dépasse pas le maximum
        player.stamina = player.MAX_STAMINA
        player.stamina_regen()
        assert player.stamina == player.MAX_STAMINA

    def test_update_animation(self, player):
        """Teste la mise à jour de l'animation"""
        initial_sprite = player.current_sprite_index
        player._update_animation(0.5)
        assert player.current_sprite_index == (initial_sprite + 0.5) % 4

    def test_check_bounds(self, player, mock_game):
        """Teste la vérification des limites"""
        # Position valide
        valid_pos = pygame.math.Vector2(
            mock_game.settings.WINDOW_WIDTH // 2,
            mock_game.settings.WINDOW_HEIGHT // 2,
        )
        assert player._check_bounds(valid_pos) is True

        # Position invalide
        invalid_pos = pygame.math.Vector2(
            mock_game.settings.WINDOW_WIDTH + 100,
            mock_game.settings.WINDOW_HEIGHT + 100,
        )
        assert player._check_bounds(invalid_pos) is False

    def test_handle_boundary_collision(self, player):
        """Teste la gestion des collisions avec les bords"""
        initial_health = player.health
        player.position = pygame.math.Vector2(-10, -10)

        player._handle_boundary_collision(player.BORDER_DAMAGE)

        assert player.health < initial_health
        assert player.position.x >= 0
        assert player.position.y >= 0

    @pytest.mark.parametrize(
        "direction,expected_movement",
        [
            (Direction.UP, (0, -1)),
            (Direction.DOWN, (0, 1)),
            (Direction.LEFT, (-1, 0)),
            (Direction.RIGHT, (1, 0)),
        ],
    )
    def test_move_directions(self, player, direction, expected_movement):
        """Teste le mouvement dans toutes les directions"""
        initial_pos = pygame.math.Vector2(100, 100)
        player.position = initial_pos
        player.speed = 5
        player.direction = direction

        player.move()

        expected_x = initial_pos.x + (expected_movement[0] * player.speed)
        expected_y = initial_pos.y + (expected_movement[1] * player.speed)

        assert player.position.x == pytest.approx(expected_x)
        assert player.position.y == pytest.approx(expected_y)
