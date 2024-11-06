from UIElement import UIElement
from Button import Button, MenuButton


class Menu(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.button_play = MenuButton(200, 200, "play", self.screen, self.game)

    def render(self):
        self.button_play.render()

    def hide(self):
        pass

    def reset(self):
        pass

