import pygame

from settings import Settings
from .controller import Controller
from .movement import Movement


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

        self.screen = pygame.display.set_mode(
            (
                self.settings.WINDOW_WIDTH, 
                self.settings.WINDOW_HEIGHT
            )
        )

        pygame.display.set_caption("Game")
        pygame.display.set_icon(pygame.image.load("assets/chicken.png"))

        self.clock = pygame.time.Clock()

        # Composants du jeu
        self.controller = Controller(self)
        self.movement = Movement(self)

        self.running = True


    def main(self) -> None:
        """
        Fonction principale du jeu
        """
        while self.running:
            self.events()
            self.update()
            self.draw()

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
        pass


    def draw(self) -> None:
        """
        Fonction pour dessiner les éléments du jeu
        """
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)
