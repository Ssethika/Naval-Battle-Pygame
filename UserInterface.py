from Enums import ShipType, ship_sizes
from Button import ShipButton
from Text import Text

from UIElement import UIElement

class Ui(UIElement):
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.is_placing_ships = True
        self.hidden = False
        self.text_selected_ship = Text(650, 450, "None", self.screen, self.game)
        self.text_current_player = Text(275, 620, "Current: Player", self.screen, self.game)
        self.text_score = Text(400, 620, "", self.screen, self.game)
        self.corvette_button = ShipButton((200, 20, 20), 640, 10, "Corvette: 2", self.screen, ShipType.CORVETTE, self.game)
        self.frigate_button = ShipButton((200, 20, 20), 640, 100, "Frigate:  3", self.screen, ShipType.FRIGATE, self.game)
        self.destroyer_button = ShipButton((200, 20, 20), 640, 190, "Destroyer:  3", self.screen, ShipType.DESTROYER, self.game)
        self.cruiser_button = ShipButton((200, 20, 20), 640, 280, "Cruiser:  4", self.screen, ShipType.CRUISER, self.game)
        self.aircraft_carrier_button = ShipButton((200, 20, 20), 640, 370, "Carrier:  5", self.screen, ShipType.AIRCRAFT_CARRIER, self.game)

        self.ui_elements_placing_ships = [self.text_selected_ship, *self.ship_buttons_list]
        self.ui_elements_placing_ships = [self.text_selected_ship, *self.ship_buttons_list]
        print(self.ui_elements_placing_ships)

        #self.ship_buttons_list = [self.corvette_button, self.frigate_button, self.destroyer_button, self.cruiser_button, self.aircraft_carrier_button]

    @property
    def ship_buttons_list(self):
        return [self.corvette_button, self.frigate_button, self.destroyer_button, self.cruiser_button, self.aircraft_carrier_button]

    def run(self):
        self.render()
        self.update()

    def reset(self):
        for ui_element in self.ui_elements_placing_ships:
            ui_element.reset()

    def render(self):
        if not self.hidden:
            self.ship_button_render()
        self.text_selected_ship.render()
        self.text_current_player.render()
        if self.game.is_attacking_ships is True:
            self.text_score.text_literal = f"Score: {self.game.current_player.score}"
            self.text_score.render()

    def hide(self):
        self.is_placing_ships = False
        for ui_element in self.ui_elements_placing_ships:
            ui_element.hide()
            self.screen.fill(self.game.background_color, ui_element.rect)

        self.text_current_player.hidden = True
        self.render()
        self.hidden = True

    def update(self):
        self.ship_button_update()
        if self.game.is_placing_ships is True:
            assert not self.game.is_attacking_ships

            if self.game.current_select is not None:
                self.text_selected_ship.text_literal = f"Current: {str(self.game.current_select).split('.')[-1]} {ship_sizes[self.game.current_select]}"
            else:
                self.text_selected_ship.text_literal = f"Current:  {str(self.game.current_select).split(".")[-1]} "
        elif self.game.is_attacking_ships is True:
            assert not self.game.is_placing_ships
            #self.text_selected_ship.text_literal = ""

        self.text_current_player.text_literal = "Player: 1" if self.game.current_player is self.game.player_1 else "Player: 2"

    def ship_button_update(self):
        for ship_button in self.ship_buttons_list:
            ship_button.update()

    def ship_button_render(self):
        for ship_button in self.ship_buttons_list:
            ship_button.render()

    def disable_ship_buttons(self):
        for ship_button in self.ship_buttons_list:
            ship_button.enabled = False
