import pygame
from UserInterface import Ui
from Terrain import Terrain
from Enums import GameState, Direction

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


# Main game class implementation.
class Game:
    def __init__(self):


        self.game = self
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Initialising UI.
        self.ui = Ui(self.screen, self.game)

        # List of all placed ships which is useful to guarantee that there is no duplicate
        self.chosen_ships = []

        # Variable that keeps track of which button is pressed
        self.pressed_ship_button = None
        self.game_state = GameState.ACTIVE
        self.terrain_1 = Terrain(self.screen, self)
        self.terrain_2 = Terrain(self.screen, self)
        self.current_select = None
        self.selecting = False
        self.running = True

    def run(self):
        # The main event loop.
        # Setup pygame, clock and screen.
        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()

        self.terrain_1.draw_line()

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.handle_events()
            # fill the screen with a color to wipe away anything from last frame

            self.screen.fill("black")

            self.terrain_1.render()
            self.terrain_1.handle_hover()
            self.terrain_1.draw_line()
            self.ui.run()

            # flip() the display to put your work on screen
            pygame.display.flip()
            clock.tick(30) # limits FPS to 30`
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Check if the player presses one of the arrow keys and execute the commands.
            self.check_keydown(event, self.current_select)

            # Check if the state of the game is active and wait for the player to press the arrow key to confirm the selection of the ship.
            if self.game_state == GameState.ACTIVE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.selecting:
                            if self.pressed_ship_button is None:
                                return
                            if self.terrain_1.is_terrain_selected() is False:
                                return
                            print("key pressed")
                            self.terrain_1.select_confirm()
                            self.pressed_ship_button.color = (128, 128, 128) # Color the button in grey.
                            self.game_state = GameState.ACTIVE

    def check_keydown(self, event, ship_type):
       # if ship_type in self.chosen_ships:
        #    print("Ship is already placed")
        #    return

       # Choose which type of preview you want to choose based on ship_type and key pressed.
        if self.current_select is None:
            print("You have not selected any ship. Please select one.")
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.terrain_1.terrain_clear()
                self.preview(Direction.UP, ship_type)

            elif event.key == pygame.K_RIGHT:
                self.terrain_1.terrain_clear()
                self.preview(Direction.RIGHT, ship_type)

            elif event.key == pygame.K_DOWN:
                self.terrain_1.terrain_clear()
                self.preview(Direction.DOWN, ship_type)

            elif event.key == pygame.K_LEFT:
                self.terrain_1.terrain_clear()
                self.preview(Direction.LEFT, ship_type)

    def preview(self, direction, ship_type):

        # Gets the current game_state.

        # If game_state is already in PLACE quit by not letting enter any further.
        if self.game_state == GameState.PLACE:
            return

        # Change the mode of the game to PLACE
        self.game_state = GameState.PLACE

        # Get the current mouse position.
        mouse_pos = pygame.mouse.get_pos()

        # Set the hit to false as default
        hit = False

        # Loop through all the cells in terrain_cells and check if at least one has been hit, If yes set the hit to True.
        for row in self.terrain_1.terrain_cells:
            for cell in row:
                if cell.rect.collidepoint(mouse_pos):
                    hit = True

        # If hit is false, which means that click was outside the terrain containing the cells, reset the game_state to ACTIVE again and do nothing.
        if not hit:
            self.game_state = GameState.ACTIVE

        # Else place the preview of the ship.
        elif hit:
            for row in self.terrain_1.terrain_cells:
                for cell in row:
                    if cell.rect.collidepoint(mouse_pos):
                        self.terrain_1.place_ship(ship_type, (cell.pos_x, cell.pos_y), direction, self)

    def choose_ship_type(self, ship_type):
        self.current_select = ship_type