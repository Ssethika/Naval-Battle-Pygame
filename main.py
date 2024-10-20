import pygame
from Game import Game

# Entry point to the program. Create game class and call Update by running main.
def main():
    game = Game()
    game.update()

    pygame.quit()

if __name__ == "__main__":
    pygame.display.set_caption("Naval Battle Game")
    main()