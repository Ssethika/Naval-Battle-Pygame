import pygame

from UIElement import UIElement
from Button import MenuButton
from Text import Text

class StartMenu(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.text = Text(310, 200, "Naval Battle Game: Choose a mode.", self.screen, self.game, size=30)
        self.button_play = MenuButton(300, 400, "play pvp", self.screen, self.game.run, self.game)
        self.button_play_ai = MenuButton(500, 400, "play pvAI", self.screen, self.game.choose_ai_skill_level, self.game)
        self.button_quit = MenuButton(700, 400, "Quit", self.screen, self.quit, self.game)
        self.rendering = True

    def quit(self):
        pygame.quit()

    def render(self):
        if self.rendering:
            self.screen.fill("black")
            self.text.render()
            self.button_play.render()
            self.button_play_ai.render()
            self.button_quit.render()
            pygame.display.flip()
            self.game.clock.tick(30)

    def disable(self):
        print("Disable")
        self.button_play_ai.enabled = False
        self.button_play.enabled = False
        self.button_quit.enabled = False
        self.hide()

    def hide(self):
        self.rendering = False

    def reset(self):
        self.rendering = True
        self.button_play.enabled = True
        self.button_play_ai.enabled = True

