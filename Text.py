import pygame
import pygame.font
from Renderable import Renderable
from UIElement import UIElement

class Text(UIElement):
     def __init__(self, pos_x, pos_y, text, screen, game):
         pygame.font.init()
         self._pos_x = pos_x
         self._pos_y = pos_y
         self.initial_text_literal = text
         self._text_literal = text
         self.font = pygame.font.SysFont('grand9kpixelregular', 20)
         self.text_surface = self.font.render(self._text_literal, False, (255, 255, 255))
         self.rect = self.text_surface.get_rect()
         self.screen = screen
         self.game = game
         self.hidden = False

     @property
     def coords(self):
        return (self._pos_x, self._pos_y)

     @coords.setter
     def coords(self, coords):
         self._pos_x = coords[0]
         self._pos_y = coords[1]

     def render(self):
        if not self.hidden:
            self.screen.blit(self.text_surface, self.coords)

     def reset(self):
         self._text_literal = self.initial_text_literal

     def hide(self):
         self.hidden = True
         self.pos_y = 2000
         self.pos_x = 2000
         print("hidden")
         self.text_literal = " "
         #self.text_surface = self.font.render("", False, (0,0,0))

     @property
     def text_literal(self):
          return self._text_literal


     @text_literal.setter
     def text_literal(self, text_literal):
          self._text_literal = text_literal
          self.text_surface = self.font.render(self._text_literal, False, (255, 255, 255))

import pygame
import pygame.font
from Renderable import Renderable
from UIElement import UIElement

class Text(UIElement):
     def __init__(self, pos_x, pos_y, text, screen, game):
         pygame.font.init()
         self._pos_x = pos_x
         self._pos_y = pos_y
         self.initial_text_literal = text
         self._text_literal = text
         self.font = pygame.font.SysFont('grand9kpixelregular', 20)
         self.text_surface = self.font.render(self._text_literal, False, (255, 255, 255))
         self.rect = self.text_surface.get_rect()
         self.screen = screen
         self.game = game
         self.hidden = False

     @property
     def coords(self):
        return (self._pos_x, self._pos_y)

     @coords.setter
     def coords(self, coords):
         self._pos_x = coords[0]
         self._pos_y = coords[1]

     def render(self):
        if not self.hidden:
            self.screen.blit(self.text_surface, self.coords)

     def reset(self):
         self._text_literal = self.initial_text_literal

     def hide(self):
         self.hidden = True
         self._pos_y = 2000
         self._pos_x = 2000
         print("hidden")
         self.text_literal = " "
         #self.text_surface = self.font.render("", False, (0,0,0))

     @property
     def text_literal(self):
          return self._text_literal


     @text_literal.setter
     def text_literal(self, text_literal):
          self._text_literal = text_literal
          self.text_surface = self.font.render(self._text_literal, False, (255, 255, 255))
