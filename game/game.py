import pygame
from typing import Optional
from enum import Enum, auto
from settings import Settings
from .controller import Controller
from .movement import Movement
from .map import Map
from .interface import Interface
from .player import Player
from .item import Item


class GameState(Enum):
    """
    Enumeration pour les états du jeu
    """

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    """
    Classe pour gérer le jeu
    """

    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings
        self._initialize_display()

        self._create_layers()

        self.clock = pygame.time.Clock()
        self._init_game_components()

        self._prev_player_rect: Optional[pygame.Rect] = None
        self.running = True
        self.state = GameState.MENU

    def _initialize_display(self) -> None:
        """
        Initialisation de l'affichage général du jeu
        """
        info = pygame.display.Info()

        if self.settings.IS_FULLSCREEN:
            self.settings.WINDOW_WIDTH = info.current_w
            self.settings.WINDOW_HEIGHT = info.current_h
            self.settings.TILE_SIZE = self.settings.WINDOW_WIDTH // 40

        self.screen = pygame.display.set_mode(
            (self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT),
            pygame.FULLSCREEN
            if self.settings.IS_FULLSCREEN
            else pygame.SCALED,
        )

        pygame.display.set_caption("Game")
        icon = pygame.image.load("assets/chicken.png").convert_alpha()
        pygame.display.set_icon(icon)

    def _create_layers(self) -> None:
        """
        Crée les différentes couches de rendu du jeu
        """
        size = (self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)

        self.background_layer = pygame.Surface(size).convert()

        self.sprite_layer = pygame.Surface(
            size, pygame.SRCALPHA
        ).convert_alpha()

        self.menu_background = None

    def _init_game_components(self) -> None:
        """
        Initialisation des composants du jeu
        """
        self.player = Player(self, "Poulet")
        self.controller = Controller(self)
        self.movement = Movement(self)
        self.map = Map(self)
        self.interface = Interface(self)
        self.item = Item(self)

        # Dessine la carte pour la première fois
        self._init_background()

    def _init_background(self) -> None:
        """
        Initialise le fond du jeu
        (appelé une fois lors de l'entrée dans le menu)
        """
        self.background_layer.fill((0, 0, 0))  # Efface le fond
        self.map.draw(self.background_layer)  # Dessine la carte

    def _init_menu_background(self) -> None:
        """
        Initialise le fond du menu
        (appelé une fois lors de l'entrée dans le menu)
        """
        if self.menu_background is None:
            # Charge et redimensionne l'image de fond du menu
            background = pygame.image.load("assets/images/menu.jpg").convert()

            # Redimensionne l'image pour qu'elle remplisse l'écran
            scale = max(
                self.settings.WINDOW_WIDTH / background.get_width(),
                self.settings.WINDOW_HEIGHT / background.get_height(),
            )

            new_size = (
                int(background.get_width() * scale),
                int(background.get_height() * scale),
            )

            self.menu_background = pygame.transform.scale(background, new_size)

            # Charge et redimensionne le texte du menu
            self.menu_text = pygame.image.load(
                "assets/images/menu_text.png"
            ).convert_alpha()
            max_width = self.settings.WINDOW_WIDTH // 3 * 2

            text_scale = max_width / self.menu_text.get_width()
            text_size = (
                max_width,
                int(self.menu_text.get_height() * text_scale),
            )

            self.menu_text = pygame.transform.scale(self.menu_text, text_size)

    def main_menu(self) -> None:
        """
        Affiche le menu principal du jeu
        """
        self._init_menu_background()
        pygame.display.set_caption("Menu")

        # Calule la position du texte du menu
        text_x = (
            self.settings.WINDOW_WIDTH // 2 - self.menu_text.get_width() // 2
        )
        text_y = self.settings.WINDOW_HEIGHT - self.menu_text.get_height() - 50

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.main()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            if self.running:
                self.screen.blit(self.menu_background, (0, 0))
                self.screen.blit(self.menu_text, (text_x, text_y))
                pygame.display.flip()
                self.clock.tick(self.settings.FPS)

    def main(self) -> None:
        """
        Fonction principale du jeu
        """
        pygame.display.set_caption("Game")

        while self.running:
            self.events()
            self.update()
            self.optimized_draw()

        pygame.quit()

    def events(self) -> None:
        """
        Gère les événements du jeu
        """
        for event in pygame.event.get():
            self.controller.event(event)

    def update(self) -> None:
        """
        Met à jour les composants du jeu
        """
        self.player.move()
        self.player.heal()
        self.player.stamina_regen()
        self.interface.update()

    def optimized_draw(self) -> None:
        """
        Affichage optimisé du jeu
        """
        # Efface l'ancienne position du joueur
        self.sprite_layer.fill((0, 0, 0, 0))

        # Affiche le joueur à sa nouvelle position
        self.player.draw(self.sprite_layer)

        self.screen.blit(self.background_layer, (0, 0))
        self.screen.blit(self.sprite_layer, (0, 0))  # Draw sprites

        # Affiche l'interface
        self.interface.draw()
        self.item.draw()

        pygame.display.flip()
        self.clock.tick(self.settings.FPS)
