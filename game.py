import pygame
from tile import *
from board import *

pygame.init()

win = pygame.display.set_mode((250, 250))
pygame.display.set_caption("2048")
speed = 10


def new_background():
    bg = pygame.Surface((250, 250))
    bg.fill((205, 193, 180))

    for pos in range(5):
        pos = pos * 60
        pygame.draw.rect(bg, (187, 173, 160), (0, pos, 250, 10))

    for pos in range(5):
        pos = pos * 60
        pygame.draw.rect(bg, (187, 173, 160), (pos, 0, 10, 250))

    return bg


def run_simple_ai():
    run = True

    new_board = Board()
    while run:

        pygame.time.delay(100)
        new_board = simple_ai(new_board)
        this_background = new_background()

        for this_tile in new_board.tiles:
            this_background.blit(this_tile.get_tile(), this_tile.position)

        win.blit(new_background(), (0, 0))
        win.blit(this_background, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


def run_manual():

    new_board = Board()
    this_background = new_background()
    for this_tile in new_board.tiles:
        this_background.blit(this_tile.get_tile(), this_tile.position)
    win.blit(this_background, (0, 0))
    pygame.display.update()

    while not game_over(new_board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                new_board = update_board(new_board, event.key)
                this_background = new_background()
                for this_tile in new_board.tiles:
                    this_background.blit(this_tile.get_tile(), this_tile.position)
                win.blit(this_background, (0, 0))
                pygame.display.update()
                # new_board = update_board(new_board, event.key)
                # new_board.print_board()
                # print()


background = new_background()

board = Board()
for tile in board.tiles:
    x = tile.position[0]
    y = tile.position[1]
    background.blit(tile.get_tile(), (x, y))

win.blit(background, (0, 0))
pygame.display.update()

if __name__ == '__main__':
    run_simple_ai()
    pygame.quit()
