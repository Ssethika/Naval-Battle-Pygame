from typing import Tuple

import pygame
from Cell import Cell
from Enums import CellType, Direction, GameState, ship_sizes, ShipType
from Renderable import Renderable


class Terrain(Renderable):

    # Should start to initialise the terrain_cells with cells in it with the default type of water.
    def __init__(self, screen, game, border_color):
        self.game = game
        self.screen = screen
        self._is_hidden = False
        self.border_color = border_color
        self.terrain_cells = [[Cell(x, y, CellType.WATER, self.screen) for x in range(10)] for y in range(10)]

        #Used only during the attacking phase of the game
        self.clicked = False

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, is_hidden):
        for row in self.terrain_cells:
            for cell in row:
                cell.is_hidden = True
        self._is_hidden = is_hidden

    # draw the lines of the terrain.
    def draw_line(self):
        for z in range(11):
            pygame.draw.line(self.screen, self.border_color, (10, 0 + z * 60 + 10), (610, 0 + z * 60 + 10))

        for w in range(11):
            pygame.draw.line(self.screen, self.border_color, (0 + w * 60 + 10, 10), (0 + w * 60 + 10, 610))

    # Render each cell of the terrain
    def render(self):
        for row in self.terrain_cells:
            for cell in row:
                cell.render()

    # Confirm the cell placement by turning all the SELECT cell type to SHIP.
    def select_confirm(self):

        if self.game.current_select.name in self.game.chosen_ships:
            print("You have already placed this ship")
            return

        for row in self.terrain_cells:
            for cell in row:
                if cell.state == CellType.SELECT:
                    cell.state = CellType.SHIP

        self.game.selecting_cells = False

        self.game.chosen_ships.append(self.game.current_select.name)

    def select_confirm_ai(self):

        for row in self.terrain_cells:
            for cell in row:
                if cell.state == CellType.SELECT:
                    cell.state = CellType.SHIP

    def clear(self):
        for row in self.terrain_cells:
            for cell in row:
                if cell.state == CellType.HOVER or cell.state == CellType.SELECT:
                    cell.state = CellType.WATER

    def is_selected(self):
        for row in self.terrain_cells:
            for cell in row:
                if cell.state == CellType.SELECT:
                    return True
        return False

    # Function that handle mouse hovering of a cell.
    def handle_hover(self):
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Loop through each cell and check if the mouse is over it
        for row in self.terrain_cells:
            for cell in row:
                if cell.rect.collidepoint(mouse_pos):
                    # If the mouse is over a cell, temporarily change its color (e.g., light blue for hover)
                    pygame.draw.rect(self.screen, CellType.HOVER.value, cell.rect)
                else:
                    # Otherwise, render the cell with its default color
                    cell.render()

    """The main function that handles ship placement. TODO: Separate this function into smaller functions."""
    def place_ship(self, ship_type, coordinate, direction, game):
        """

        :param ship_type:
        :param coordinate:
        :param direction:
        :param game:
        """
        ship_size = ship_sizes[ship_type]
        is_chosen_start_ship = False

        # cx and cy are the two coordinates of the cells that go pressed.
        # IMPORTANT: cy goes from top to bottom in order.
        cx = coordinate[1]
        cy = coordinate[0]
        print(coordinate[0], coordinate[1], ship_type)
        chosen_start = self.terrain_cells[coordinate[1]][coordinate[0]]
        if chosen_start.state is CellType.SHIP:
            is_chosen_start_ship = True

        #chosen_start.set_cell_state(CellType.HOVER)

        is_colliding = False
        # TODO: We really need to extract this into a function.
        #check if the first selected cell has the state of ship at the beginning
        if not is_chosen_start_ship:
            if direction == Direction.RIGHT:
                if self.terrain_cells[cx][cy].pos_x + ship_size <= 10:
                    # Check if the hovered cells collide with a Cell ship
                    for y in range(ship_size):
                        if self.terrain_cells[cx][cy + y].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")
                    # If not make the next 4 cell depending on the direction Hovered
                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx][cy + x].state = CellType.SELECT
                        self.game.selecting_cells = True

            elif direction is Direction.LEFT:
                if self.terrain_cells[cx][cy].pos_x - ship_size >= -1:
                    for y in range(ship_size):
                        if self.terrain_cells[cx][cy - y].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")

                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx][cy - x].state = CellType.SELECT
                        self.game.selecting_cells = True

            elif direction is Direction.UP:
                if self.terrain_cells[cx][cy].pos_y - ship_size >= -1:
                    for y in range(ship_size):
                        if self.terrain_cells[cx - y][cy].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")

                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx - x][cy].state = CellType.SELECT
                        self.game.selecting_cells = True


            elif direction is Direction.DOWN:
                if self.terrain_cells[cx][cy].pos_y + ship_size <= 10:
                    for y in range(ship_size):
                        if self.terrain_cells[cx + y][cy].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")
                        self.game.selecting_cells = True


                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx + x][cy].state = CellType.SELECT
                        self.game.selecting_cells = True

        game.game_state = GameState.ACTIVE


    def place_ship_ai(self, ship_type: ShipType, coordinate: Tuple[int, int], direction: Direction, game):
        """

        :param ship_type: ShipType
        :param coordinate: Tuple[int, int]
        :param direction: Direction
        :param game: Game
        """
        ship_size: int = ship_sizes[ship_type]
        is_chosen_start_ship: bool = False

        # cx and cy are the two coordinates of the cells that go pressed.
        # IMPORTANT: cy goes from top to bottom in order.
        cx = coordinate[1]
        cy = coordinate[0]
        print(coordinate[0], coordinate[1], ship_type)
        chosen_start = self.terrain_cells[coordinate[1]][coordinate[0]]
        if chosen_start.state is CellType.SHIP:
            is_chosen_start_ship = True
            return "Collided"

        #chosen_start.set_cell_state(CellType.HOVER)
        is_colliding = False
        # TODO: We really need to extract this into a function.
        #check if the first selected cell has the state of ship at the beginning
        if not is_chosen_start_ship:
            if direction == Direction.RIGHT:
                if self.terrain_cells[cx][cy].pos_x + ship_size <= 10:
                    # Check if the hovered cells collide with a Cell ship
                    for y in range(ship_size):
                        if self.terrain_cells[cx][cy + y].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")
                            return "Collided"
                    # If not make the next 4 cell depending on the direction Hovered
                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx][cy + x].state = CellType.SELECT
                        self.game.selecting_cells = True

            elif direction is Direction.LEFT:
                if self.terrain_cells[cx][cy].pos_x - ship_size >= -1:
                    for y in range(ship_size):
                        if self.terrain_cells[cx][cy - y].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")
                            return "Collided"

                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx][cy - x].state = CellType.SELECT
                        self.game.selecting_cells = True

            elif direction is Direction.UP:
                if self.terrain_cells[cx][cy].pos_y - ship_size >= -1:
                    for y in range(ship_size):
                        if self.terrain_cells[cx - y][cy].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")
                            return "Collided"

                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx - x][cy].state = CellType.SELECT
                        self.game.selecting_cells = True

            elif direction is Direction.DOWN:
                if self.terrain_cells[cx][cy].pos_y + ship_size <= 10:
                    for y in range(ship_size):
                        if self.terrain_cells[cx + y][cy].state == CellType.SHIP:
                            is_colliding = True
                            print(f"Colliding: {is_colliding}")
                            return "Collided"
                        self.game.selecting_cells = True

                    if not is_colliding:
                        for x in range(ship_size):
                            self.terrain_cells[cx + x][cy].state = CellType.SELECT
                        self.game.selecting_cells = True

        game.game_state = GameState.ACTIVE
        return "Success"