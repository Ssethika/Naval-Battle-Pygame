import pygame

from UIElement import UIElement
from Button import MenuButton


class StartMenu(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.button_play = MenuButton(200, 200, "play pvp", self.screen, self.game.run, self.game)
        self.button_play_ai = MenuButton(400, 200, "play pvAI", self.screen, self.game.run_ai, self.game)
        self.button_quit = MenuButton(600, 200, "Quit", self.screen, pygame.quit, self.game)
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

