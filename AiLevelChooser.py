import pygame

from UIElement import UIElement
from Button import MenuButton
from Text import Text

class AiLevelChooser(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.text = Text(400, 200, "Choose an AI difficulty", self.screen, self.game, 30)
        self.button_stupid_ai = MenuButton(300, 300, "Stupid", self.screen, lambda: self.game.run_ai(self.game.handle_ai_stupid_ship_attack_events), self.game)
        self.button_smart_ai = MenuButton(500, 300, "Smart", self.screen, lambda: self.game.run_ai(self.game.handle_ai_smart_ship_attack_events), self.game)
        self.button_quit = MenuButton(700, 300, "Quit", self.screen, self.quit, self.game)
        self.rendering = True

    def quit(self):
        pygame.quit()

    def render(self):
        if self.rendering:
            self.screen.fill("black")
            self.text.render()
            self.button_smart_ai.render()
            self.button_stupid_ai.render()
            self.button_quit.render()
            pygame.display.flip()
            self.game.clock.tick(30)

    def disable(self):
        print("Disable StartMenu")
        self.button_stupid_ai.enabled = False
        self.button_smart_ai.enabled = False
        self.button_quit.enabled = False
        self.hide()

    def hide(self):
        self.rendering = False

    def reset(self):
        self.rendering = True
        self.button_stupid_ai.enabled = True
        self.button_smart_ai.enabled = True
        self.button_quit = True


