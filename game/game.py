import pygame

from settings import Settings
from .controller import Controller
from .movement import Movement
from .map import Map
from .interface import Interface
from .player import Player


class Game:
    """
    Classe principal du jeu
    """

    def __init__(self) -> None:
        """
        Constructeur de la classe
        """
        pygame.init()

        self.settings = Settings
        info = pygame.display.Info()
        if self.settings.IS_FULLSCREEN:
            self.settings.WINDOW_WIDTH = info.current_w
            self.settings.WINDOW_HEIGHT = info.current_h
            self.settings.TILE_SIZE = self.settings.WINDOW_WIDTH // 40

        self.screen = pygame.display.set_mode(
            (self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT),
            pygame.FULLSCREEN if self.settings.IS_FULLSCREEN else 0,
        )

        pygame.display.set_caption("Game")
        pygame.display.set_icon(pygame.image.load("assets/chicken.png"))

        self.clock = pygame.time.Clock()

        # Composants du jeu
        self.player = Player(
            self,
            "Poulet",
        )
        self.controller = Controller(self)
        self.movement = Movement(self)
        self.map = Map(self)
        self.interface = Interface(self)

        self.running = True

    def main_menu(self) -> None:
        """
        Fonction pour afficher le menu principal
        """
        pygame.display.set_caption("Menu")

        while self.running:
            # Set the background image for the menu
            background = pygame.image.load("assets/images/menu.jpg")
            # Resize the image to fit the screen and preserve the aspect ratio
            background = pygame.transform.scale(
                background,
                (
                    self.settings.WINDOW_WIDTH,
                    int(
                        background.get_height()
                        * self.settings.WINDOW_WIDTH
                        / background.get_width()
                    ),
                ),
            )
            if background.get_height() < self.settings.WINDOW_HEIGHT:
                background = pygame.transform.scale(
                    background,
                    (
                        int(
                            background.get_width()
                            * self.settings.WINDOW_HEIGHT
                            / background.get_height()
                        ),
                        self.settings.WINDOW_HEIGHT,
                    ),
                )

            self.screen.blit(background, (0, 0))

            # Create the buttons
            text = pygame.image.load("assets/images/menu_text.png")
            # Max width of the text
            max_width = self.settings.WINDOW_WIDTH // 3 * 2
            # Resize the text to fit the screen
            text = pygame.transform.scale(
                text,
                (
                    max_width,
                    int(text.get_height() * max_width / text.get_width()),
                ),
            )

            self.screen.blit(
                text,
                (
                    self.settings.WINDOW_WIDTH // 2 - text.get_width() // 2,
                    self.settings.WINDOW_HEIGHT - text.get_height() - 50,
                ),
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.main()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            if self.running:
                pygame.display.flip()

    def main(self) -> None:
        """
        Fonction principale du jeu
        """
        pygame.display.set_caption("Game")

        while self.running:
            self.events()
            self.draw()
            self.update()

        pygame.quit()

    def events(self) -> None:
        """
        Fonction pour gérer les événements
        """
        for event in pygame.event.get():
            self.controller.event(event)

    def update(self) -> None:
        """
        Fonction pour mettre à jour les éléments du jeu
        """
        self.player.move()
        self.interface.update()

    def draw(self) -> None:
        """
        Fonction pour dessiner les éléments du jeu
        """
        pygame.display.flip()
        self.map.draw(self.screen)
        self.player.draw(self.screen)
        self.clock.tick(self.settings.FPS)
