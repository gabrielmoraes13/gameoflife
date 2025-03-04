import pygame 


class GameScreen():
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.BOARD_WIDTH = 600
        self.BOARD_HEIGHT = 400
        self.GRID_SIZE = 10
        self.CELL_SIZE = 60
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

    
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('The Game of Life')
