import pygame

from Renderable import Renderable

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 60
PADDING = 10

class Cell(Renderable):
    """
    The cell object of the game. The cell has a state  and a position on the board
    """
    def __init__(self, pos_x, pos_y, state, screen):

        self.rect = pygame.Rect(0 + pos_x * CELL_SIZE + PADDING, pos_y * CELL_SIZE + PADDING, CELL_SIZE, CELL_SIZE)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._state = state
        self.color = state.value
        self.screen = screen
        self.hit = False
        self._is_hidden = False

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, is_hidden):
        print("is_hidden")
        self._is_hidden = is_hidden

    @property
    def position(self):
        """
        Give a tuple of the position in the board of the cell.
        :return: tuple: (integer, integer)
        """
        return self.pos_x, self.pos_y

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        """
        :param state: Enum CellType

        Sets the state and also the color as the state value.
        Doing this cause Enums in python are weird,
        """
        self._state = state
        self.color = state.value

     # Rendering each cell based on color and rectangle
    def render(self) -> None:
        """
        Render the cell.

        :rtype: object
        """
        if self.is_hidden:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)

    def reveal(self) -> None:
        """
        Reveal the cell if hidden
        """
        self.hit = True
        self.is_hidden = False
        pass