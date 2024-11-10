import pygame
from pygame import SurfaceType

from UIElement import UIElement
from Button import MenuButton
from Text import Text

class ReplayMenu(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.ending_text: Text = Text(100, 100, f"{str(self.game.winning_player)} Has won", self.screen, self.game)
        self.button_replay = MenuButton(200, 200, "Replay", self.screen, self.game.replay, self.game)
        self.button_quit = MenuButton(400, 200, "Quit", self.screen, pygame.quit, self.game)
        self.rendering = True

    def render(self):
        self.ending_text.text_literal = f"{str(self.game.winning_player.name)} Has Won!!!!!!!!"

        self.screen.fill("black")

        self.ending_text.render()
        self.button_replay.render()
        self.button_quit.render()

        pygame.display.flip()
        self.game.clock.tick(30)

    def hide(self):
        self.button_replay.enabled = False
        self.button_quit.enabled = False
        self.rendering = False

    def reset(self):
        pass