import pygame
from tile import *
from board import *


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
    pygame.init()
    win = pygame.display.set_mode((250, 250))
    pygame.display.set_caption("2048")
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


def run_simple_ai_fast():
    run = True

    new_board = Board()
    while run:
        new_board = simple_ai(new_board, True, 3)[0]
        if game_over(new_board):
            return new_board

    return new_board


def simple_ai_stats():
    num_tests = 100
    total_tests = num_tests
    scores = list()

    while num_tests is not 0:
        this_board = run_simple_ai_fast()
        score = this_board.get_highest()
        scores.append(score)
        num_tests -= 1

    statistics = dict()

    for score in scores:
        if score in statistics:
            statistics[score] += 1
        else:
            statistics[score] = 1

    temp_stats = sorted(statistics)
    temp_stats.reverse()
    sorted_statistics = dict()

    for stat in temp_stats:
        percent = statistics[stat] / total_tests
        percent_string = "%" + str(int(percent * 100))
        sorted_statistics[stat] = percent_string

    print(sorted_statistics)


def run_expectimax():
    pygame.init()
    win = pygame.display.set_mode((250, 250))
    pygame.display.set_caption("2048")

    run = True

    new_board = Board()
    while run:
        new_board = expectimax(new_board, True, 2)[0]
        win.blit(new_background(), (0, 0))
        this_background = new_background()
        for tile in new_board.tiles:
            this_background.blit(tile.get_tile(), tile.position)
        win.blit(this_background, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    return new_board()


def run_expectimax_fast():
    run = True

    new_board = Board()
    while run:
        new_board = expectimax(new_board, True, 3)[0]
        if game_over(new_board):
            return new_board


def run_expectimax_stats():
    num_tests = 10
    total_tests = num_tests
    scores = list()

    while num_tests is not 0:
        this_board = run_expectimax_fast()
        score = this_board.get_highest()
        scores.append(score)
        num_tests -= 1
        print(num_tests)

    statistics = dict()

    for score in scores:
        if score in statistics:
            statistics[score] += 1
        else:
            statistics[score] = 1

    temp_stats = sorted(statistics)
    temp_stats.reverse()
    sorted_statistics = dict()

    for stat in temp_stats:
        percent = statistics[stat] / total_tests
        percent_string = "%" + str(int(percent * 100))
        sorted_statistics[stat] = percent_string

    print(sorted_statistics)


def run_manual():
    pygame.init()
    win = pygame.display.set_mode((250, 250))
    pygame.display.set_caption("2048")

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


if __name__ == '__main__':
    run_expectimax_stats()
