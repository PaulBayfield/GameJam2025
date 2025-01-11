import pygame

from settings import WINDOW_HEIGHT, WINDOW_WIDTH, FPS


class Game:
    """
    Classe principal du jeu
    """
    def __init__(self) -> None:
        """
        Constructeur de la classe
        """
        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                WINDOW_WIDTH, 
                WINDOW_HEIGHT
            )
        )

        pygame.display.set_caption("Game")

        self.clock = pygame.time.Clock()

        self.running = True


    def main(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        pygame.quit()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self):
        pass


    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.main()
