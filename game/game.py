import pygame

from settings import Settings
from .components.controller import Controller
from .components.movement import Movement
from .components.map import Map
from .components.interface import Interface
from .components.player import Player
from .components.item import Item
from .enums.game import GameState
from .enemies.enemy_spawner import EnemySpawner
from .utils.stats import Stats
from typing import Optional
from datetime import datetime


class Game:
    """
    Classe pour gérer le jeu
    """

    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings
        self.settings.ITEM_SIZE = self.settings.TILE_SIZE * 1.8

        self.mixer = pygame.mixer
        self.footsteps = self.mixer.Sound("assets/songs/sfx/chicken_run.mp3")
        self.current_song = 0
        self.playlist = [
            "assets/songs/music/1.mp3",
            "assets/songs/music/2.mp3",
        ]
        self._initialize_display()

        self._create_layers()

        self.clock = pygame.time.Clock()
        self._init_game_components()

        self._prev_player_rect: Optional[pygame.Rect] = None
        self.running = True
        self.paused = False
        self.state = GameState.CINEMATIC

        self.stats = Stats()

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
        self.enemy_spawner = EnemySpawner(self)

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

    def start_cinematic(self) -> None:
        """
        Lance la cinématique de début du jeu
        """
        self.interface.cinematic()

    def main_menu(self) -> None:
        """
        Affiche le menu principal du jeu
        """
        self._init_menu_background()
        pygame.display.set_caption("Menu")
        self.mixer.music.load("assets/songs/music/menu.mp3")
        self.mixer.music.play(-1)
        self.mixer.music.set_volume(0.3)

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

                # Display stats
                stats_text = self.stats.get_formatted_stats()
                font = pygame.font.SysFont(None, 36)
                y_offset = 50
                for line in stats_text.splitlines():
                    stats_surface = font.render(line, True, (255, 255, 255))
                    self.screen.blit(stats_surface, (20, y_offset))
                    y_offset += 40

                pygame.display.flip()
                self.clock.tick(self.settings.FPS)

    def play_in_game_music(self) -> None:
        """
        Joue la musique du jeu
        """
        self.mixer.music.load(self.playlist[self.current_song])
        self.mixer.music.play()
        self.mixer.music.set_volume(0.3)
        self.mixer.music.set_endevent(pygame.USEREVENT + 1)

    def main(self) -> None:
        """
        Fonction principale du jeu
        """
        pygame.display.set_caption("Game")
        # Jouer 3 musique à la suite (en boucle)

        self.play_in_game_music()

        self.footsteps.set_volume(0.1)
        self.footsteps.play(-1)

        self.stats.update("gamesPlayed", 1)

        self.state = GameState.PLAYING
        self.start_time = datetime.now()

        while self.running:
            self.events()
            self.update()
            self.optimized_draw()

        if self.state == GameState.END:
            print("end")
            pygame.quit()
        elif self.state == GameState.GAME_OVER:
            pass

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
        if self.state == GameState.PLAYING:
            self.player.move()
            self.player.on_fire()
            self.player.isAttacked()
            self.player.heal()
            self.player.stamina_regen()
            self.interface.update()
            self.enemy_spawner.update()
        elif self.state == GameState.GAME_OVER:
            self.stats.update("deaths", 1)

            self.end_time = datetime.now()
            self.stats.update(
                "secondsPlayed", (self.end_time - self.start_time).seconds
            )

            self.footsteps.stop()
            self.interface.end((self.end_time - self.start_time).seconds)
            self.running = False
        elif self.state == GameState.PAUSED:
            if not self.paused:
                self.paused = True
                self.footsteps.stop()
                self.interface.paused()
        elif self.state == GameState.END:
            self.end_time = datetime.now()
            self.footsteps.stop()
            self.stats.update(
                "secondsPlayed", (self.end_time - self.start_time).seconds
            )

            self.running = False
            self.state = GameState.MENU
            self.reset()
            self.main_menu()

    def optimized_draw(self) -> None:
        """
        Affichage optimisé du jeu
        """
        if self.state == GameState.PLAYING:
            # Efface l'ancienne position du joueur
            self.sprite_layer.fill((0, 0, 0, 0))

            self.screen.blit(self.background_layer, (0, 0))
            self.enemy_spawner.draw(self.sprite_layer)  # Draw enemies
            self.screen.blit(self.sprite_layer, (0, 0))  # Draw sprites

            # Affiche le joueur à sa nouvelle position
            self.player.draw(self.sprite_layer)
            self.player.draw_damage(self.sprite_layer)

            self.screen.blit(self.background_layer, (0, 0))
            self.screen.blit(self.sprite_layer, (0, 0))  # Draw sprites

            # Affiche l'interface
            self.interface.draw()
            self.item.draw()

            pygame.display.flip()
            self.clock.tick(self.settings.FPS)

    def reset(self) -> None:
        """
        Réinitialise le jeu
        """
        self._init_game_components()
        self.running = True
        self.paused = False
        self._prev_player_rect = None
