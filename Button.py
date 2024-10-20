from abc import abstractmethod, ABC
from Renderable import Renderable
import pygame
import pygame.font

class ButtonInterface(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def check_if_clicked(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_click(self):
        pass

class Button(ButtonInterface, Renderable):
    def __init__(self, color, pos_x, pos_y, width, height, text, screen, game):
        pygame.font.init()
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.font = pygame.font.SysFont('grand9kpixelregular', 20)
        self.text = text
        self.text_surface = self.font.render(text, False, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.clicked = False

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

        pygame.draw.line(self.screen, (255, 255, 255), (self.pos_x, self.pos_y), (self.pos_x + self.width , self.pos_y))
        pygame.draw.line(self.screen, (255, 255, 255),(self.pos_x + self.width, self.pos_y), (self.pos_x + self.width, self.pos_y +self.height))
        pygame.draw.line(self.screen, (255, 255, 255),(self.pos_x, self.pos_y + self.height), (self.pos_x + self.width, self.pos_y +self.height))
        pygame.draw.line(self.screen, (255, 255, 255), (self.pos_x, self.pos_y),(self.pos_x, self.pos_y + self.height))

        self.screen.blit(self.text_surface, self.text_rect)

    def check_if_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == False:
                self.clicked = True
                self.on_click()

        if pygame.mouse.get_pressed()[0] == 1:
            self.clicked = False

    @abstractmethod
    def on_click(self):
        pass

    def update(self):
        self.check_if_clicked()

class ShipButton(Button):
    def __init__(self, color, pos_x, pos_y, text, screen, ship_type, game):
        super().__init__(color, pos_x, pos_y, 160, 60, text, screen, game)
        self.ship_type = ship_type

    def on_click(self):
        self.game.choose_ship_type(self.ship_type)