import pygame

from UIElement import UIElement
from Button import MenuButton


class StartMenu(UIElement):

    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.button_play = MenuButton(200, 200, "play pvp", self.screen, self.game.run, self.game)
        self.button_play_ai = MenuButton(400, 200, "play pvAI", self.screen, self.game.run_ai, self.game)
        self.button_quit = MenuButton(600, 200, "Quit", self.screen, self.quit, self.game)
        self.rendering = True

    def quit(self):
        pygame.quit()

    def render(self):
        if self.rendering:
            print("0 Menu Render Initialized: ", pygame.display.get_init())
            self.screen.fill("black")
            print("1 Menu Render Initialized: ", pygame.get_init())
            print("1 Menu Render Initialized: ", pygame.display.get_init())
            self.button_play.render()
            print("2 Menu Render Initialized: ", pygame.get_init())
            print("2 Menu Render Initialized: ", pygame.display.get_init())
            self.button_play_ai.render()
            print("3 Menu Render Initialized: ", pygame.get_init())
            print("3 Menu Render Initialized: ", pygame.display.get_init())
            self.button_quit.render()
            print("4 Menu Render Initialized: ", pygame.get_init())
            print("4 Menu Render Initialized: ", pygame.display.get_init())
            print("2 Menu Render Initialized: ", pygame.get_error())
            pygame.display.flip()
            print("5 Menu Render Initialized: ", pygame.display.get_init())
            self.game.clock.tick(30)
            print("4 Menu Render Initialized: ", pygame.get_init())
            print("4 Menu Render Initialized: ", pygame.display.get_init())

    def disable(self):
        print("Rendering StartMenu")
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

