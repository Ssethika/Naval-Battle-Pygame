import pygame

from UIElement import UIElement
from Button import MenuButton


class ReplayMenu(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.text: str = "End"
        self.button_play = MenuButton(200, 200, "Replay", self.screen, self.game.run, self.game)
        self.button_quit = MenuButton(400, 200, "Quit", self.screen, pygame.quit, self.game)
        self.rendering = True

    def render(self):
        self.screen.fill("black")
        self.button_play.render()
        self.button_play_ai.render()
        self.button_quit.render()

        pygame.display.flip()
        self.game.clock.tick(30)

    def hide(self):
        self.button_play_ai.enabled = False
        self.button_play_ai.enabled = False
        self.rendering = False

    def reset(self):
        pass