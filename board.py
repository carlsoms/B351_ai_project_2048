import copy

import pygame
import random
from tile import *


class Board:
    def __init__(self):
        new_board = list()
        empty_spaces = list()

        for x in range(4):
            row = list()
            for y in range(4):
                row.append(0)
                empty_spaces.append((x, y))
            new_board.append(row)

        self.board = new_board
        self.empty_spaces = empty_spaces
        self.tiles = list()
        add_random_tile(self)
        add_random_tile(self)

    def copy(self):
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.empty_spaces = self.empty_spaces.copy()
        new_board.tiles = self.tiles.copy()
        return new_board

    def print_board(self):
        for x in self.board:
            for y in x:
                print(y, end=" ")
            print()

    def insert_tile(self, position, tile):

        current_board = self.board
        new_board = list()

        for x in range(4):
            row = list()
            if position[0] == x:
                for y in range(4):
                    if position[1] == y:
                        row.append(tile)
                    else:
                        row.append(current_board[x][y])
            else:
                row = current_board[x]
            new_board.append(row)

        self.board = new_board
        self.empty_spaces.remove(position)

    def equals(self, other_board):
        for x in range(4):
            for y in range(4):
                if self.board[x][y] != other_board.board[x][y]:
                    return False
        return True


def update_empty(this_board):
    matrix = this_board.board.copy()
    new_empty = list()

    for x in range(4):
        for y in range(4):
            if matrix[x][y] == 0:
                new_empty.append((x, y))

    return new_empty


def update_tile(this_board):
    matrix = this_board.board.copy()
    new_tiles = list()

    for x in range(4):
        for y in range(4):
            if matrix[x][y] != 0:
                new_tile = Tile(matrix[x][y], (y, x))
                new_tiles.append(new_tile)

    return new_tiles


def update_board(this_board, key):
    new_board = Board()
    temp_board = this_board.copy()
    matrix = this_board.board[:]
    new_board.board = shift(matrix, key)
    for x in range(4):
        for y in range(4):
            if matrix[x][y] != new_board.board[x][y]:
                new_board.empty_spaces = update_empty(new_board)
                add_random_tile(new_board)
                new_board.empty_spaces = update_empty(new_board)
                new_board.tiles = update_tile(new_board)
                return new_board

    new_board.tiles = update_tile(new_board)
    new_board.empty_spaces = update_empty(new_board)
    return new_board


def shift(input_matrix, key):
    new_matrix = list()
    this_matrix = input_matrix.copy()
    if key == pygame.K_LEFT:
        for row in this_matrix:
            new_row = row.copy()
            new_row = shift_row(new_row)
            new_matrix.append(new_row)

    if key == pygame.K_RIGHT:
        for row in this_matrix:
            new_row = row.copy()
            new_row.reverse()
            new_row = shift_row(new_row)
            new_row.reverse()
            new_matrix.append(new_row)

    if key == pygame.K_UP:
        temp_matrix = list()
        new_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for x in range(4):
            new_row = list()
            for y in range(4):
                new_row.append(copy.copy(this_matrix[y][x]))
            new_row = shift_row(new_row)
            temp_matrix.append(new_row)

        for x in range(4):
            new_row = list()
            for y in range(4):
                new_matrix[x][y] = copy.copy(temp_matrix[y][x])

    if key == pygame.K_DOWN:
        temp_matrix = list()
        new_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for x in range(4):
            new_row = list()
            for y in range(4):
                new_row.append(this_matrix[y][x])
            new_row.reverse()
            new_row = shift_row(new_row)
            new_row.reverse()
            temp_matrix.append(new_row)

        for x in range(4):
            new_row = list()
            for y in range(4):
                new_matrix[x][y] = temp_matrix[y][x]

    return new_matrix


def shift_row(this_row):
    new_row = list()
    for value in this_row:
        if value != 0:
            new_row.append(value)

    index = 0
    merged_row = list()
    while index < len(new_row):
        if index + 1 < len(new_row) and new_row[index] == new_row[index + 1]:
            new_value = int(new_row[index])
            new_value *= 2
            merged_row.append(new_value)
            index += 2
        else:
            merged_row.append(new_row[index])
            index = index + 1
    for index in range(4):
        if index >= len(merged_row):
            merged_row.append(0)

    return merged_row


def add_random_tile(this_board):
    tile_choices = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]

    value = random.choice(tile_choices)
    position = random.choice(this_board.empty_spaces)

    tile = Tile(value, position)
    this_board.tiles.append(tile)
    this_board.insert_tile(position, value)
    return tile


def movable(tiles, key):
    if key == pygame.K_LEFT:
        pos = 0
        bound = 10
        direction = -6
    elif key == pygame.K_RIGHT:
        pos = 0
        bound = 190
        direction = 6
    elif key == pygame.K_UP:
        pos = 1
        bound = 10
        direction = -6
    else:
        pos = 1
        bound = 190
        direction = 6

    return can_move(pos, bound, tiles, direction)


def can_move(variable, bound, tiles, direction):
    current_tiles = tiles

    for tile in current_tiles:
        if tile.position[variable] != bound:
            for tile2 in current_tiles:
                if tile.position[variable] + (move_speed * direction) == tile2.position[variable]:
                    if tile.position[0] == tile2.position[0] or tile.position[1] == tile2.position[1]:
                        return False
            return True

    return False


def game_over(this_board):
    new_board = this_board.copy()
    new_board = update_board(new_board, pygame.K_LEFT)
    new_board = update_board(new_board, pygame.K_UP)
    new_board = update_board(new_board, pygame.K_RIGHT)
    new_board = update_board(new_board, pygame.K_DOWN)

    if this_board.equals(new_board):
        return True
    else:
        return False


def simple_ai(this_board):
    if not this_board.equals(update_board(this_board, pygame.K_LEFT)):
        return update_board(this_board, pygame.K_LEFT)
    elif not this_board.equals(update_board(this_board, pygame.K_UP)):
        return update_board(this_board, pygame.K_UP)
    elif not this_board.equals(update_board(this_board, pygame.K_RIGHT)):
        return update_board(this_board, pygame.K_RIGHT)
    elif not this_board.equals(update_board(this_board, pygame.K_DOWN)):
        return update_board(this_board, pygame.K_DOWN)
    else:
        return this_board



