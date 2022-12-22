import pygame

from isometric_game.game import Game


def main(game: Game):
    game.run()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Isometric Game')
    game = Game()
    main(game)
