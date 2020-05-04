import copy
import math

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
        self.empty_spaces = update_empty(self)
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
        update_empty(self)
        update_tile(self)

    def equals(self, other_board):
        for x in range(4):
            for y in range(4):
                if self.board[x][y] != other_board.board[x][y]:
                    return False
        return True

    def get_highest(self):
        highest = 0

        for x in range(4):
            for y in range(4):
                if self.board[x][y] > highest:
                    highest = self.board[x][y]

        return highest


def calc_score(this_board):
    total_score = 0
    this_matrix = this_board.board.copy()

    for x in range(4):
        for y in range(4):
            total_score += this_matrix[x][y]

    return total_score / 16


def calc_heuristic(this_board):
    weight_matrix = [[math.pow(4, 16), math.pow(4, 15), math.pow(4, 14), math.pow(4, 13)],
                     [math.pow(4, 9), math.pow(4, 10), math.pow(4, 11), math.pow(4, 12)],
                     [math.pow(4, 8), math.pow(4, 7), math.pow(4, 6), math.pow(4, 5)],
                     [math.pow(4, 1), math.pow(4, 2), math.pow(4, 3), math.pow(4, 4)]]

    total = 0
    for x in range(4):
        for y in range(4):
            this_tile = this_board.board[x][y]
            total += (this_tile * weight_matrix[x][y])

    return total * calc_score(this_board)


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


def expectimax(this_board, max_node, depth):
    if game_over(this_board) or depth == 0:
        return this_board, calc_heuristic(this_board)
    elif max_node:
        return maximum(this_board, depth)
    else:
        return expect(this_board, depth)


def expect(this_board, depth):
    for tile_value in range(2):
        if tile_value == 1:
            prob = .9
        else:
            prob = .1
        value = 0
        this_board.empty_spaces = update_empty(this_board)
        for successor in this_board.empty_spaces:
            new_prob = prob * (1 / len(this_board.empty_spaces))
            new_board = this_board.copy()
            new_board.insert_tile(successor, tile_value * 2)

            value += new_prob * expectimax(new_board, True, depth - 1)[1]

    return this_board, value


def maximum(this_board, depth):
    value = this_board, float("-inf")
    successors = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
    for successor in successors:
        test_board = this_board.copy()
        if not update_board(test_board, successor).equals(this_board):
            temp_matrix = shift(this_board.board.copy(), successor)
            temp_board = Board()
            temp_board.board = temp_matrix
            update_tile(temp_board)
            update_empty(temp_board)

            new_value = (temp_board, expectimax(temp_board, False, depth - 1)[1])
            if new_value[1] > value[1]:
                value = successor, new_value[1]

    return update_board(this_board, value[0]), value[1]

