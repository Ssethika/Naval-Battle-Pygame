import random
from random import randint
from typing import Tuple
import pygame
from pygame import SurfaceType
from pygame.mixer import SoundType
from pygame.time import Clock
import UserInterface
from Button import Button
from ReplayMenu import ReplayMenu
from StartMenu import StartMenu
from AiLevelChooser import AiLevelChooser
from Player import Player
from UserInterface import Ui
from Terrain import Terrain
from Enums import GameState, Direction, CellType, ShipType, ship_sizes

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MISSED_REVEAL_DELAY_EVENT = pygame.USEREVENT + 1
HIT_REVEAL_DELAY_EVENT = pygame.USEREVENT + 2
FINISH_DELAY_EVENT = pygame.USEREVENT + 3
AI_HIT_SMART_REVEAL_DELAY_EVENT = pygame.USEREVENT + 4
AI_MISSED_REVEAL_DELAY_EVENT = pygame.USEREVENT + 5
AI_HIT_STUPID_REVEAL_DELAY_EVENT = pygame.USEREVENT + 6

# Main game class implementation.
class Game:
    """
       Main class for the game that handles initialization, game state, event handling,
       and running the main game loop.
    """
    def __init__(self):
        """
            Initializes the game by setting up the screen, background, menus, and sound mixer.
        """
        self.screen: SurfaceType = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_color: Tuple[int, int, int] = (0, 0, 0)
        self.initialize_game()
        self.menu: UserInterface = StartMenu(self.screen, self)
        self.replay_menu: UserInterface = ReplayMenu(self.screen, self)
        self.ai_level_chooser_menu: UserInterface = AiLevelChooser(self.screen, self)
        pygame.init()
        pygame.mixer.init()

    def de_initialize_game(self):
        """
            Clears game variables and objects for resetting or ending the game.
        """
        del self.ui
        del self.chosen_ships
        del self.pressed_ship_button
        del self.terrain_1
        del self.terrain_2
        del self.player_1
        del self.player_2
        del self.current_player
        del self.winning_player

    def initialize_game(self):
        """
            Initializes UI, players, terrains, and game state variables for a new game session.
        """
        # Initialising UI.
        self.ui: Ui = Ui(self.screen, self)
        self.clicked: bool = False
        # List of all placed ships which is useful to guarantee that there is no duplicate
        self.chosen_ships: list[ShipType] = []
        self.is_placing_ships: bool = True
        self.is_attacking_ships: bool = False
        # Variable that keeps track of which button is pressed
        self.pressed_ship_button: Button | None = None
        self.game_state: GameState = GameState.ACTIVE

        self.terrain_1: Terrain = Terrain(self.screen, self, (200, 0, 0))
        self.terrain_2: Terrain = Terrain(self.screen, self, (0, 0, 200))

        self.player_1: Player = Player(self.terrain_1, "Player 1")
        self.player_2: Player = Player(self.terrain_2, "Player 2")
        self.current_player: Player = self.player_1
        self.colliding: bool | None = None
        self.current_select: bool | None = None
        self.selecting_cells: bool = False
        self.running: bool = True
        self.in_menu: bool = True
        self.in_replay_menu: bool = False
        self.in_difficulty_choosing_menu: bool = False
        self.winning_player: Player | None = None
        self.clock: Clock = pygame.time.Clock()
        self.explosion_sound: SoundType = pygame.mixer.Sound("assets/missile-explosion.mp3")
        self.water_splash_sound: SoundType = pygame.mixer.Sound("assets/water-splash.mp3")

        # Temporary solution for storing what was the cell that was.
        self.last_hit_cell_ship: Tuple[int, int] | None = None
        # pygame.init()
        # pygame.mixer.init()
    def sound_play(self, sound):
        """
            Plays a given sound and stops any background music.

        Parameters:
            sound: The sound effect to play.
        """
        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    def choose_ai_skill_level(self) -> None:
        """
            Activates the AI skill level menu, allowing the player to choose the AI difficulty.
        """
        self.in_difficulty_choosing_menu = True
        self.in_menu = False
        self.menu.disable()
        while self.in_difficulty_choosing_menu is True:
            self.ai_level_chooser_menu.render()
            self.handle_quit()


    def replay(self) -> None:
        """
            Resets the game state to allow for replaying, reinitializing all relevant variables and UI elements.
        """
        self.de_initialize_game()
        self.reset()
        self.in_menu = True
        self.menu.reset()
        self.play()

    def reset(self) -> None:
        """
            Reinitialize the game screen and background, preparing the game for a fresh start.
        """
        self.initialize_game()

    def play(self) -> None:
        """
            Handles the main game loop for the 'play' state where the player interacts with the menu.
        """
        self.in_replay_menu = False
        while self.in_menu is True:
            self.handle_quit()
            self.menu.render()

    def run(self) -> None:
        """
            Starts the main game loop for gameplay events, including handling quitting, ship placement,
            and attacks, updating screen visuals, and tracking player scores.
        """
        self.in_menu = False
        self.menu.disable()
        while self.running:

            if self.in_replay_menu is False:
                if self.is_placing_ships:
                    # Place the ships in the game
                    self.place_ships()
                    # Set game state to attacking
                    self.game_state = GameState.ATTACKING
                self.screen.fill("black")
                self.ui.run()
                self.handle_events()
                self.current_player.terrain.render()
                #self.current_player.terrain.handle_hover()
                self.current_player.terrain.draw_line()
                self.handle_ship_attack_events()

                if self.current_player.score >= 17:
                    # Finish the game
                    self.winning_player = self.current_player
                    self.in_replay_menu = True
                    self.running = False

                # flip() the display to put your work on screen
                pygame.display.flip()
                self.clock.tick(30) # limits FPS to 30`
        # Drop back to replay menu when game is finish
        while self.in_replay_menu is True:
            self.handle_quit()
            self.replay_menu.render()
    pygame.quit()

    def run_ai(self, ai_attack_function):
        """
            Runs the game with AI logic, allowing AI attacks and player attacks in turn until a win condition is met.

            Parameters:
                ai_attack_function: The AI's attack strategy function to execute each turn.
        """
        self.in_difficulty_choosing_menu = False
        self.current_player = self.player_1
        self.menu.disable()
        pygame.init()
        pygame.mixer.init()
        clock: Clock = pygame.time.Clock()

        # Place each ship automatically.
        self.ai_auto_place(ShipType.CORVETTE)
        self.ai_auto_place(ShipType.FRIGATE)
        self.ai_auto_place(ShipType.DESTROYER)
        self.ai_auto_place(ShipType.CRUISER)
        self.ai_auto_place(ShipType.AIRCRAFT_CARRIER)
        while self.running:
            while self.is_placing_ships:
                # self.ui.text_current_player.render()
                self.current_player = self.player_2
                self.handle_ship_placing_events()
                # fill the screen with a color to wipe away anything from last frame

                self.screen.fill("black")

                self.player_2.terrain.render()
                self.player_2.terrain.handle_hover()
                self.player_2.terrain.draw_line()
                if self.ui.is_placing_ships:
                    self.ui.run()
                # self.is_placing_ships = False
                if len(self.chosen_ships) >= 5 and self.current_player is self.player_2:
                    # Change to the player.
                    self.chosen_ships = []
                    self.ui.reset()
                    self.current_player = self.player_1
                    self.player_1.terrain.is_hidden = True
                    self.player_2.terrain.is_hidden = True
                    self.ui.disable_ship_buttons()
                    for button in self.ui.ship_buttons_list:
                        button.disable()
                    self.ui.text_selected_ship.coords = (650, 10)
                    self.is_placing_ships = False
                    self.is_attacking_ships = True
                    self.game_state = GameState.ATTACKING

                pygame.display.flip()
                clock.tick(30)
            self.screen.fill("black")
            self.ui.run()
            self.handle_events()
            self.current_player.terrain.render()
            self.current_player.terrain.handle_hover()
            self.current_player.terrain.draw_line()
            if self.current_player is self.player_1:
                self.handle_ship_attack_events()
            else:
                ai_attack_function()
            if self.current_player.score >= 17:
                self.running = False
                self.in_replay_menu = True
                self.winning_player = self.player_1 if self.current_player is self.player_2 else self.player_2
            # flip() the display to put your work on screen
            pygame.display.flip()
            clock.tick(30)  # limits FPS to 30`
        while self.in_replay_menu is True:
            self.handle_quit()
            self.replay_menu.render()

        pygame.quit()

    def handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.ui.disable()

            if event.type == MISSED_REVEAL_DELAY_EVENT:
                self.handle_timer_event(event)

            if event.type == HIT_REVEAL_DELAY_EVENT:
                self.handle_timer_event(event)

            if event.type == FINISH_DELAY_EVENT:
                self.handle_timer_event(event)

            if event.type == AI_HIT_SMART_REVEAL_DELAY_EVENT:
                self.handle_timer_event(event)

            if event.type == AI_MISSED_REVEAL_DELAY_EVENT:
                self.handle_timer_event(event)

            if event.type == AI_HIT_STUPID_REVEAL_DELAY_EVENT:
                self.handle_timer_event(event)

    def handle_ai_stupid_ship_attack_events(self):
        selected_cell_coords = (randint(0, 9), randint(0, 9))

        if self.current_player.terrain.clicked is False:
            # selected_cell_coords = (randint(0, 9),randint(0, 9))
            cell = self.current_player.terrain.terrain_cells[selected_cell_coords[0]][selected_cell_coords[1]]
            if cell.hit is True:
                self.handle_ai_smart_ship_attack_events()
            if cell.state == CellType.SUNK:
                self.handle_ai_smart_ship_attack_events()
            elif cell.state == CellType.WATER:
                self.ui.text_selected_ship.text_literal = "Missed!! "
                cell.reveal()
                self.current_player.shots += 1
                self.current_player.terrain.clicked = True
                self.sound_play(self.water_splash_sound)
                pygame.time.set_timer(AI_MISSED_REVEAL_DELAY_EVENT, 500)

            elif cell.state == CellType.SHIP:
                self.current_player.terrain.clicked = True
                cell.state = CellType.SUNK
                self.ui.text_selected_ship.text_literal = "Shot!! "
                self.current_player.score += 1
                cell.reveal()
                self.current_player.shots += 1
                self.sound_play(self.explosion_sound)
                pygame.time.set_timer(AI_HIT_STUPID_REVEAL_DELAY_EVENT, 1000)

    def handle_ai_smart_ship_attack_events(self, selected_cell_coords=None):
        if selected_cell_coords is None:
            selected_cell_coords = (randint(0, 9), randint(0, 9))

        if self.current_player.terrain.clicked is False:
            # selected_cell_coords = (randint(0, 9),randint(0, 9))
            cell = self.current_player.terrain.terrain_cells[selected_cell_coords[0]][selected_cell_coords[1]]
            if cell.hit is True:
                self.handle_ai_smart_ship_attack_events()
            if cell.state == CellType.SUNK:
                self.handle_ai_smart_ship_attack_events()
            elif cell.state == CellType.WATER:
                self.ui.text_selected_ship.text_literal = "Missed!! "
                cell.reveal()
                self.current_player.shots += 1
                self.current_player.terrain.clicked = True
                self.sound_play(self.water_splash_sound)
                pygame.time.set_timer(AI_MISSED_REVEAL_DELAY_EVENT, 1000)

            elif cell.state == CellType.SHIP:
                self.current_player.terrain.clicked = True
                cell.state = CellType.SUNK
                self.ui.text_selected_ship.text_literal = "Shot!! "
                self.current_player.score += 1
                cell.reveal()
                self.current_player.shots += 1
                self.last_hit_cell_ship = (selected_cell_coords[0], selected_cell_coords[1])
                self.sound_play(self.explosion_sound)
                pygame.time.set_timer(AI_HIT_SMART_REVEAL_DELAY_EVENT, 1000)

    def handle_ship_attack_events(self):
        for row in self.current_player.terrain.terrain_cells:
            for cell in row:
                mouse_pos = pygame.mouse.get_pos()
                if self.current_player.terrain.clicked is False:
                    if cell.rect.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed()[0] == 1:
                            if cell.hit is True:
                                return
                            if cell.state == CellType.WATER:
                                self.ui.text_selected_ship.text_literal = "Missed!! "
                                self.current_player.shots += 1
                                self.sound_play(self.water_splash_sound)
                                cell.reveal()
                            elif cell.state == CellType.SHIP:
                                self.current_player.shots += 1
                                cell.state = CellType.SUNK
                                self.ui.text_selected_ship.text_literal = "Shot!! "
                                if cell.hit is False:
                                    self.current_player.score += 1
                                    cell.reveal()
                                    self.sound_play(self.explosion_sound)
                            elif cell.state == CellType.SUNK:
                                return

                            self.current_player.terrain.clicked = True
                            if cell.state == CellType.SUNK:
                                pygame.time.set_timer(HIT_REVEAL_DELAY_EVENT, 1000)
                            elif cell.state == CellType.WATER:
                                pygame.time.set_timer(MISSED_REVEAL_DELAY_EVENT, 1000)

                    if pygame.mouse.get_pressed()[0] == 0:
                        self.current_player.terrain.clicked = False

    def handle_timer_event(self, event):
        if event.type == MISSED_REVEAL_DELAY_EVENT:
            # Switch players after the delay
            # Stop the timer so it doesn't keep firing
            self.current_player = self.player_2 if self.current_player is self.player_1 else self.player_1
            self.current_player.terrain.clicked = False
            pygame.time.set_timer(MISSED_REVEAL_DELAY_EVENT, 0)
        elif event.type == HIT_REVEAL_DELAY_EVENT:
            self.current_player.terrain.clicked = False
            pygame.time.set_timer(HIT_REVEAL_DELAY_EVENT, 0)
        elif event.type == FINISH_DELAY_EVENT:
            self.running = False
            pygame.time.set_timer(FINISH_DELAY_EVENT, 0)
        elif event.type == AI_MISSED_REVEAL_DELAY_EVENT:
            self.player_1.terrain.clicked = False
            self.current_player = self.player_1
            pygame.time.set_timer(AI_MISSED_REVEAL_DELAY_EVENT, 0)
        elif event.type == AI_HIT_STUPID_REVEAL_DELAY_EVENT:
            self.handle_ai_stupid_ship_attack_events()
            self.current_player.terrain.clicked = False
            pygame.time.set_timer(AI_HIT_STUPID_REVEAL_DELAY_EVENT, 0)
        elif event.type == AI_HIT_SMART_REVEAL_DELAY_EVENT:
            self.current_player.terrain.clicked = False
            pygame.time.set_timer(AI_HIT_SMART_REVEAL_DELAY_EVENT, 0)
            if self.last_hit_cell_ship[0] is None or self.last_hit_cell_ship[1] is None:
                self.handle_ai_smart_ship_attack_events()
            new_cell_target_x = self.last_hit_cell_ship[0] + random.choice([-1, 1])
            new_cell_target_y = self.last_hit_cell_ship[1] + random.choice([-1, 1])
            if randint(0, 1):
                if new_cell_target_x >= 10:
                    new_cell_target_x = 9
                elif new_cell_target_x <= -1:
                    new_cell_target_x = 0
                self.handle_ai_smart_ship_attack_events((new_cell_target_x, self.last_hit_cell_ship[1]))
            else:
                if new_cell_target_y >= 10:
                    new_cell_target_y = 9
                elif new_cell_target_y <= -1:
                    new_cell_target_y = 0
                self.handle_ai_smart_ship_attack_events((self.last_hit_cell_ship[0], new_cell_target_y))

    def handle_ship_placing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Check if the player presses one of the arrow keys and execute the commands.
            self.check_keydown(event, self.current_select)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.ui.disable()

            # Check if the state of the game is active and wait for the player to press the arrow key to confirm the selection of the ship.
            if self.game_state == GameState.ACTIVE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.selecting_cells:
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

    def place_ships(self):
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
                self.player_1.terrain.is_hidden = True
                self.player_2.terrain.is_hidden = True
                self.current_player = self.player_1
                self.ui.disable_ship_buttons()
                for button in self.ui.ship_buttons_list:
                    button.disable()
                self.ui.text_selected_ship.coords = (650, 10)
                self.is_placing_ships = False
                self.is_attacking_ships = True

            pygame.display.flip()
            self.clock.tick(30)  # limits FPS to 30`

    def ai_auto_place(self, ship_type):
        ship_size = ship_sizes[ship_type]
        while self.colliding != "Success":
            if randint(0, 1):
                self.colliding = self.player_1.terrain.place_ship_ai(ship_type, (randint(0, 10 - ship_size), randint(0, 9)), Direction.RIGHT, self)
            else:
                self.colliding = self.player_1.terrain.place_ship_ai(ship_type, (randint(0, 9), randint(0, 10 - ship_size)), Direction.DOWN, self)
            print(f"{str(ship_type)}", self.colliding)

        self.player_1.terrain.select_confirm_ai()
        self.colliding = None