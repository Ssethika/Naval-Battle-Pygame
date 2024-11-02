import time

import pygame
from Player import Player
from UserInterface import Ui
from Terrain import Terrain
from Enums import GameState, Direction, CellType

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
REVEAL_DELAY_EVENT = pygame.USEREVENT + 1


# Main game class implementation.
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_color = (0, 0, 0) # Black

        # Initialising UI.
        self.ui = Ui(self.screen, self)
        self.clicked = False
        # List of all placed ships which is useful to guarantee that there is no duplicate
        self.chosen_ships = []
        self.is_placing_ships = True
        self.is_attacking_ships = False
        # Variable that keeps track of which button is pressed
        self.pressed_ship_button = None
        self.game_state = GameState.ACTIVE

        self.terrain_1 = Terrain(self.screen, self)
        self.terrain_2 = Terrain(self.screen, self)

        self.player_1 = Player(self.terrain_1)
        self.player_2 = Player(self.terrain_2)
        self.current_player = self.player_1

        self.current_select = None
        self.selecting = False
        self.running = True


    def run(self):
        # The main event loop.
        # Setup pygame, clock and screen.
        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            if self.is_placing_ships is True:
                self.place_ships(clock)

            self.screen.fill("black")
            self.ui.run()
            self.handle_events()
            self.current_player.terrain.render()
            #self.current_player.terrain.handle_hover()
            self.current_player.terrain.draw_line()
            self.handle_ship_attack_events()
            # flip() the display to put your work on screen
            pygame.display.flip()
            clock.tick(30) # limits FPS to 30`

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.ui.hide()

            if event.type == REVEAL_DELAY_EVENT:
                self.handle_timer_event(event)

    def handle_ship_attack_events(self):
        for row in self.current_player.terrain.terrain_cells:
            for cell in row:
                mouse_pos = pygame.mouse.get_pos()
                if cell.rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        print("pressed")
                        if cell.state == CellType.WATER:
                            self.ui.text_selected_ship.text_literal = "Missed!! "
                        elif cell.state == CellType.SHIP:
                            self.ui.text_selected_ship.text_literal = "Shot!! "
                            if cell.hit is False:
                                self.current_player.score += 1
                        cell.reveal()
                        self.clicked = True
                        pygame.time.set_timer(REVEAL_DELAY_EVENT, 500)


                    if pygame.mouse.get_pressed()[0] == 0:
                        self.clicked = False

    def handle_timer_event(self, event):
        if event.type == REVEAL_DELAY_EVENT:
            self.current_player = self.player_2 if self.current_player is self.player_1 else self.player_1
            # Switch players after the delay
            # Stop the timer so it doesn't keep firing
            pygame.time.set_timer(REVEAL_DELAY_EVENT, 0)

    def handle_ship_placing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Check if the player presses one of the arrow keys and execute the commands.
            self.check_keydown(event, self.current_select)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.ui.hide()

            # Check if the state of the game is active and wait for the player to press the arrow key to confirm the selection of the ship.
            if self.game_state == GameState.ACTIVE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.selecting:
                            if self.pressed_ship_button is None:
                                return
                            if self.current_player.terrain.is_selected() is False:
                                return
                            self.current_player.terrain.select_confirm()
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
                self.current_player.terrain.clear()
                self.preview(Direction.UP, ship_type)

            elif event.key == pygame.K_RIGHT:
                self.current_player.terrain.clear()
                self.preview(Direction.RIGHT, ship_type)

            elif event.key == pygame.K_DOWN:
                self.current_player.terrain.clear()
                self.preview(Direction.DOWN, ship_type)

            elif event.key == pygame.K_LEFT:
                self.current_player.terrain.clear()
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
        for row in self.current_player.terrain.terrain_cells:
            for cell in row:
                if cell.rect.collidepoint(mouse_pos):
                    hit = True

        # If hit is false, which means that click was outside the terrain containing the cells, reset the game_state to ACTIVE again and do nothing.
        if not hit:
            self.game_state = GameState.ACTIVE

        # Else place the preview of the ship.
        elif hit:
            for row in self.current_player.terrain.terrain_cells:
                for cell in row:
                    if cell.rect.collidepoint(mouse_pos):
                        self.current_player.terrain.place_ship(ship_type, (cell.pos_x, cell.pos_y), direction, self)

    def choose_ship_type(self, ship_type):
        self.current_select = ship_type

    def place_ships(self, clock):
        while self.is_placing_ships:
            # self.ui.text_current_player.render()
            self.handle_ship_placing_events()
            # fill the screen with a color to wipe away anything from last frame

            self.screen.fill("black")

            self.current_player.terrain.render()
            self.current_player.terrain.handle_hover()
            self.current_player.terrain.draw_line()
            if self.ui.is_placing_ships:
                self.ui.run()
            # self.is_placing_ships = False
            if len(self.chosen_ships) >= 5 and self.current_player is self.player_1:
                self.chosen_ships = []
                self.ui.reset()
                self.current_player = self.player_2
            elif len(self.chosen_ships) >= 5 and self.current_player is self.player_2:
                # self.ui.reset()
                #self.ui.hide()
                #self.ui.reset()
                self.player_1.terrain.is_hidden = True
                self.player_2.terrain.is_hidden = True
                self.current_player = self.player_1
                self.ui.disable_ship_buttons()
                for button in self.ui.ship_buttons_list:
                    button.hide()
                self.ui.text_selected_ship.coords = (650, 10


                                                     )
                #self.ui.text_current_player.hide()
                self.is_placing_ships = False
                self.is_attacking_ships = True

            pygame.display.flip()
            clock.tick(30)  # limits FPS to 30`