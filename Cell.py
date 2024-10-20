import pygame

from Renderable import Renderable

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 60
PADDING = 10
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Cell(Renderable):

    # Initialization.
    def __init__(self, pos_x, pos_y, state, screen):
        # Pygame rectangle.
        self.rect = pygame.Rect(0 + pos_x * CELL_SIZE + PADDING, pos_y * CELL_SIZE + PADDING, CELL_SIZE, CELL_SIZE)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._state = state
        self.color = state.value
        self.screen = screen

    # Rendering of each cell by taking its rectangle pygame object and its color.
    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    @property
    def state(self):
        return self._state

    # Setter function that modifies the state of an object, and also it's color at the same time.
    @state.setter
    def state(self, state):
        self._state = state
        self.color = state.value