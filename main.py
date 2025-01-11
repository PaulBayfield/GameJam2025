import pygame
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, FPS

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Case By Case")
clock = pygame.time.Clock()


def main():
	running = True
	while running:
		screen.fill((0, 0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Affichage des éléments
		screen.fill((0, 0, 0))
		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()


if __name__ == "__main__":
	main()
