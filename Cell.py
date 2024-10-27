import pygame

from Renderable import Renderable

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 60
PADDING = 10

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

    @property
    def position(self):
        return self.pos_x, self.pos_y

    @property
    def state(self):
        return self._state

    """ Setter function that modifies the state of an object, and also it's color at the same time. """
    @state.setter
    def state(self, state):
        self._state = state
        self.color = state.value

     # Rendering each cell based on color and rectangle
    def render(self) -> None:
        """

        :rtype: object
        """
        pygame.draw.rect(self.screen, self.color, self.rect)