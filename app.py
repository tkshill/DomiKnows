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
    def __init__(self, side_1, side_2):

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


class Player(object):
    def __init__(self, order):
        self.order = order
        self.dominoes = []
        self.exposed = (None, None)

    def add_domino(self, domino):
        self.dominoes.append(domino)

    def check_for_completion(self):
        if self.dominoes:
            return False
        else:
            return True

    def add_remaining_dominoes(self):
        return sum((domino.size for domino in self.dominoes))


class Game(object):
    def __init__(self, size):
        dominoes = self._create_dominoes(size)

    def _create_dominoes(self, size):
        dominoes = set()
        for i in range(size + 1):
            for j in range(size + 1):
                dominoes.add(Domino(i, j))
        return dominoes

    def _create_players(self):
        number = 1

    def start(self):
        pass


def run():

    max_size = 6  # config['DEFAULT_SIZE']
    game = Game(max_size)
    game.start()


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
        attempt = run()
    except KeyboardInterrupt:
        sys.exit(-1)
    except SystemError:
        pass
    except:
        pass