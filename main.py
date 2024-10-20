import pygame
from Game import Game

def main():
    game = Game()
    game.update()

    pygame.quit()

if __name__ == "__main__":
    pygame.display.set_caption("Naval Battle Game")
    main()