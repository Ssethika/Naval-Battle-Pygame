from Renderable import Renderable
from Enums import ShipType
from Button import ShipButton

class Ui(Renderable):
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.corvette_button = ShipButton((200, 20, 20), 640, 10, "Corvette: 2", self.screen, ShipType.CORVETTE, self.game)
        self.frigate_button = ShipButton((200, 20, 20), 640, 100, "Frigate:  3", self.screen, ShipType.FRIGATE, self.game)
        self.destroyer_button = ShipButton((200, 20, 20), 640, 190, "Destroyer:  3", self.screen, ShipType.DESTROYER, self.game)
        self.cruiser_button = ShipButton((200, 20, 20), 640, 280, "Cruiser:  4", self.screen, ShipType.CRUISER, self.game)
        self.aircraft_carrier_button = ShipButton((200, 20, 20), 640, 370, "Carrier:  5", self.screen, ShipType.AIRCRAFT_CARRIER, self.game)

        self.ship_buttons_list = [self.corvette_button, self.frigate_button, self.destroyer_button, self.cruiser_button, self.aircraft_carrier_button]

    def run(self):
        self.render()
        self.update()

    def render(self):
        self.ship_button_render()

    def update(self):
        self.ship_button_update()

    def ship_button_update(self):
        for ship_button in self.ship_buttons_list:
            ship_button.update()

    def ship_button_render(self):
        for ship_button in self.ship_buttons_list:
            ship_button.render()