__author__ = 'Kirk'
__version__ = 0.1

"""
Sample application to implement a version of the dominoes game in python. Also an attempt by the creator to explore
machine learning, application development, version control, and PYTHON 3
"""

import sys
import configparser
import pathlib
from collections import OrderedDict
from random import randint
from collections import deque

config = configparser.ConfigParser()
CONFIG_NAME = 'default_config.cfg'


class Domino(object):
    """
    Object representing a single domino piece. Possesses two 'sides' for each half of the domino. Possess a side which
    is the sum of the two sides and a type which can be either normal or double.
    """

    def __init__(self, side_1, side_2, type="normal"):
        self.type = type
        self.side_1 = side_1
        self.side_2 = side_2

    def __str__(self):
        return "{} Domino: {}, {}".format(self.type, self.side_1, self.side_2)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return self.size() + other.size()

    def __call__(self, side):
        """
        if an instance is called with value 1, call returns the value of side 1. if called with 2, returns the value
        of side 2.
        """
        if side == 1:
            return self.side_1
        elif side == 2:
            return self.side_2

    def size(self):
        """
        Add both sides and return the result
        """
        return self.side_1 + self.side_2


class Board(object):
    """
    Represents a game board. Each game has one. Dominoes are transferred from the players to the board.
    """

    def __init__(self):
        self._chain = deque()
        self.ends = {'LEFT': self._chain.popleft(), 'RIGHT': self._chain.pop()}

    def is_empty(self):
        """
        Checks if Board has had any dominoes placed on it. If it's empty, returns True else return false.
        :return: Boolean value
        """
        if not len(self._chain):
            return True
        else:
            return False

    def update_board(self, domino, side, end):
        """
        Accepts a domino and a side to play it on. Adds domino to deque container chain and updates ends
        """
        chain = self._chain
        if not len(chain):
            chain.appendleft(domino.side_1)
            chain.append(domino.side_2)
            self.update_ends()
        else:
            pass

    def update_ends(self):
        """
        uses a dictionary to expose the ends of the deque... necessary?
        :return:
        """

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
        return sum((domino.size() for domino in self.dominoes))

    def make_move(self):
        board = self.board
        if board.is_empty():
            d = self.dominoes.pop()
            return d.sides, board.end1
        else:
            for domino in self.dominoes:
                if domino.side_1 == board.ends['LEFT']:
                    status = self.check_for_completion()
                    return domino, 1, 'LEFT', status
                elif domino.side_1 == board.ends['RIGHT']:
                    status = self.check_for_completion()
                    return domino, 1, 'RIGHT', status
                elif domino.side_2 == board.ends['LEFT']:
                    status = self.check_for_completion()
                    return domino, 2, 'LEFT', status
                elif domino.side_2 == board.ends['RIGHT']:
                    status = self.check_for_completion()
                    return domino, 2, 'RIGHT', status



class Game(object):

    def __init__(self, size):
        self.board = Board()
        self.player_set = [Player(order, self) for order in range(4)]

        dominoes = self._create_domino_set(size)

        for player in self.player_set:
            for count in range(7):
                rand = randint(0, len(dominoes)-1)
                player.add_domino(dominoes[rand])

    @staticmethod
    def _create_domino_set(size):
        dominoes = []
        doubles = set()
        for i in range(size + 1):
            for j in range(size + 1):
                size = i + j
                if (i == j) and (not size in doubles):
                    dominoes.append(Domino(i, j, "double"))
                    doubles.add(size)
                dominoes.append(Domino(i, j))
        return dominoes

    def end_via_block(self):
        final_score = [(player.order, player.add_remaining_dominoes()) for player in self.player_set]
        final_score.sort()

    def run(self):
        board = self.board
        skipped = 0
        while True:
            for player in self.player_set:
                try:
                    domino, side, end, win_status = player.make_move()
                    skipped = 0
                except TypeError:
                    skipped +=1
                    if skipped == 4:
                        self.end_via_block()
                else:
                    board.update(domino, side, end)
                    if win_status:
                        print("Player {} wins!!!".format(player.order))
                    return


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
        raise
    except:
        raise