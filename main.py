import pygame
import sys

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BOARD_WIDTH = 1000
BOARD_HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class GameScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The Game of Life')
        self.font = pygame.font.Font(None, 36)
        self.board_spaces = ['Start', '1', '2', '3', '4', '5', '6', '7']

    def draw_board(self):
        self.screen.fill(WHITE)
        for i, space in enumerate(self.board_spaces):
            x = (i % GRID_SIZE) * CELL_SIZE + 50
            y = (i // GRID_SIZE) * CELL_SIZE + 100
            pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
            text = self.font.render(space, True, BLACK)
            self.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 3))

def main():
    clock = pygame.time.Clock()
    screen = GameScreen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.draw_board()



        pygame.display.flip()
        clock.tick(30)


main()