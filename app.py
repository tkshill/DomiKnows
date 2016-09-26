__author__ = 'Kirk'
__version__ = 0.1

"""
Sample application to implement a version of the dominoes game in python. Also an attempt by the creator to explore
machine learning, application development, version control, and PYTHON 3
"""

import os
import sys
import doctest
import configparser
import logging
import pathlib

config = configparser.ConfigParser()
CONFIG_NAME = 'default_config.cfg'


class Domino(object):
    def __init__(self, side_1, side_2, type="normal"):
        self.type = type
        self.side_1 = side_1
        self.side_2 = side_2

    def __str__(self):
        return "Domino: {}, {}".format(self.side_1, self.side_2)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return self.size() + other.size()

    def size(self):
        return self.side_1 + self.side_2


class Board(object):
    # deque?

    def __init__(self):
        self.end1 = None
        self.end2 = None

    def is_empty(self):
        if not self.end1:
            return True
        else:
            return False


class Player(object):
    def __init__(self, order, game):
        self.board = game.board
        self.order = order
        self.dominoes = set()

    def add_domino(self, domino):
        self.dominoes.add(domino)

    def check_for_completion(self):
        if self.dominoes:
            return False
        else:
            return True

    def add_remaining_dominoes(self):
        return sum((domino.size for domino in self.dominoes))

    def make_move(self):
        if self.board.is_empty():
            d = self.dominoes.pop()
            self.board.end1 = d.side1
            self.board.end2 = d.side2


class Game(object):

    def __init__(self, size):
        self.board = Board()
        self.player_set = [Player(order, self) for order in range(4)]

        dominoes = self._create_domino_set(size)

        for player in self.player_set:
            for count in range(7):
                player.add_domino(dominoes.pop())

    @staticmethod
    def _create_domino_set(size):
        dominoes = set()
        doubles = set()
        for i in range(size + 1):
            for j in range(size + 1):
                size = i + j
                if (i == j) and (not size in doubles):
                    dominoes.add(Domino(i, j, "double"))
                    doubles.add(size)
                dominoes.add(Domino(i, j))
        return dominoes

    # @staticmethod
    # def _create_players():
    #     player_set = set()
    #     for order in range(1, 5):
    #         p = Player(order)
    #         player_set.add(p)
    #     return player_set

    def run(self):
        while True:
            for player in self.player_set:
                player.play_card()


def main():
    max_size = 6  # config['DEFAULT_SIZE']
    game = Game(max_size)
    game.run()


def make_config_file(config, config_name):
    config['DEFAULT_SIZE'] = 6
    default_size = config['DEFAULT_SIZE']

    with open(config_name, 'w') as configfile:
            config.write(default_size)


if __name__ == "__main__":

    if not pathlib.Path(CONFIG_NAME).is_file():
        # make_config_file(config, CONFIG_NAME)
        pass

    try:
        attempt = main()
    except KeyboardInterrupt:
        sys.exit(-1)
    except SystemError:
        pass
    except:
        pass