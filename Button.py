from abc import abstractmethod
from Renderable import Renderable
from Enums import ShipType
import pygame
import pygame.font

from UIElement import UIElement


class Button(UIElement):
    def __init__(self, color, pos_x, pos_y, width, height, text, screen, game):
        pygame.font.init()
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.initial_color = color
        self.color = color
        self.border_color = (255, 255, 255) # WHITE
        self.screen = screen
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.font = pygame.font.SysFont('grand9kpixelregular', 20)
        self._text = text
        self.text_surface = self.font.render(text, False, (255, 255, 255)).convert_alpha() # Convert_alpha gains a lot of performance
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.clicked = False
        self.enabled = True
        self.hidden = False

    def render_text(self):
        if not self.hidden:
            self.screen.blit(self.text_surface, self.text_rect)


    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

        pygame.draw.line(self.screen, self.border_color, (self.pos_x, self.pos_y), (self.pos_x + self.width , self.pos_y))
        pygame.draw.line(self.screen, self.border_color,(self.pos_x + self.width, self.pos_y), (self.pos_x + self.width, self.pos_y +self.height))
        pygame.draw.line(self.screen, self.border_color,(self.pos_x, self.pos_y + self.height), (self.pos_x + self.width, self.pos_y +self.height))
        pygame.draw.line(self.screen, self.border_color, (self.pos_x, self.pos_y),(self.pos_x, self.pos_y + self.height))

        self.render_text()

    def check_if_clicked(self):
        if self.enabled:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    print("pressed")
                    self.clicked = True
                    self.on_click()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def reset(self):
        self.color = self.initial_color

    def update(self):
        self.check_if_clicked()

    def hide(self):
        self.color = self.game.background_color
        self.border_color = self.game.background_color
        self.hidden = True


    @abstractmethod
    def on_click(self):
        pass

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()
        print(self._text)


class ShipButton(Button):
    def __init__(self, color, pos_x, pos_y, text, screen, ship_type, game):
        super().__init__(color, pos_x, pos_y, 160, 60, text, screen, game)
        self.ship_type = ship_type

    def on_click(self):
        self.game.current_player.terrain.clear()
        self.game.choose_ship_type(ShipType[self.ship_type.name])
        self.game.pressed_ship_button = self

    def check_if_ship_not_placed(self):
        if self.ship_type.name not in self.game.chosen_ships:
            return True
        else:
            print(self.ship_type, self.game.chosen_ships)
            print("You already chose this ship")
            return False
