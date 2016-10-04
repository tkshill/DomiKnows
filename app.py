__author__ = 'Kirk'
__version__ = 0.1

"""
Sample application to implement a version of the dominoes game in python. Also an attempt by the creator to explore
machine learning, application development, version control, and PYTHON 3
"""

import sys
import configparser
import pathlib
import logging
from random import randint
from collections import deque
import traceback
import unittest
from unittest import mock
import time
from collections import defaultdict

# TODO write doctests/unittests for all available methods
# TODO subclass player to make human player
# TODO Move players initialization outside of game so same players can play multiple games...
# TODO add command line arguments so game can be started with 4 comp players or 3 comp one human player
# TODO GUI/NO GUI? Kivy or tkinter
# TODO Machine learnin'

config = configparser.ConfigParser()
CONFIG_NAME = 'default_config.cfg'
LOGGING_FILE = 'domi_knows.log'

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)


class MyException(Exception):
    pass


class CannotPlay(MyException):
    """
    Custom Exception Cannot Play when the player's dominoes match up to no dominoes on the board
    """
    pass


class DominoArgValueError(MyException):
    """
    Raise when domino is called with incorrect args
    """
    pass


class BoardArgValueError(MyException):
    pass


class Domino(object):
    """
    Object representing a single domino piece. Possesses two 'sides' for each half of the domino. Possess a size which
    is the sum of the two sides and a type which can be either normal or double.
    """

    def __init__(self, side_1, side_2):
        self.side_1 = side_1
        self.side_2 = side_2

    def __str__(self):
        return "Domino: {}, {}".format(self.side_1, self.side_2)

    def __repr__(self):
        return self.__str__()

    def __call__(self, side):
        """
        if an instance is called with value 1, call returns the value of side 1. if called with 2, returns the value
        of side 2. Mainly to expedite checking whether a domino matches ends without having to refer to side1 and side2.
        """
        if side == 1:
            return self.side_1
        elif side == 2:
            return self.side_2
        else:
            raise DominoArgValueError('Domino call arguments can either be 1 or 2')

    def size(self):
        """
        Add both sides and return the result
        """
        return self.side_1 + self.side_2


class Board(object):
    """
    Represents a game board. Each game has one. Players can inspect tiles on board. Dominoes are transferred from the
    players to the board.
    """
    def __init__(self):
        self._chain = deque()

    def is_empty(self):
        """
        Checks if Board has had any dominoes placed on it. If it's empty, returns True else return false.
        :return: Boolean value
        """
        if not len(self._chain):
            return True
        else:
            return False

    def update_board(self, domino, d_side, b_end):
        """
        Accepts a domino and a side to play it on. Adds domino to deque container chain and updates ends
        """
        chain = self._chain
        if d_side == 1:
            if b_end == "left":
                chain.appendleft(domino.side_1)
                chain.appendleft(domino.side_2)
            elif b_end == "right":
                chain.append(domino.side_1)
                chain.append(domino.side_2)
        elif d_side == 2:
            if b_end == "left":
                chain.appendleft(domino.side_2)
                chain.appendleft(domino.side_1)
            elif b_end == "right":
                chain.append(domino.side_2)
                chain.append(domino.side_1)

        print("Board status: {}".format(chain))


    def __call__(self, end):
        """
        Insert 'left' or 'right' to get one end of the chain or another.
        """
        if end == 'left':
            return self._chain[0]
        elif end == 'right':
            return self._chain[-1]
        else:
            raise BoardArgValueError(
                'incorrect argument to Board, use either "left" or "right".'
            )


class Player(object):
    """
    Player represents exactly what you think. Each player has a set of dominoes, a game which they are a part of
    (and thus access to viewing the game's board). Players can make moves and (eventually) analyze the board to make the
    best moves.
    """
    def __init__(self, order, board):
        self.board = board
        self.order = order
        self.dominoes = set()

    def add_domino(self, domino):
        """
        Adds a single domino to the set of dominoes.
        """
        self.dominoes.add(domino)

    def check_for_completion(self):
        """
        Checks if player has played all the dominoes given at the start of the game/Checks if their dominoes_set is
        empty. Returns True or False
        """
        if self.dominoes:
            return False
        else:
            return True

    def add_remaining_dominoes(self):
        """
        Returns the sum of the remaining dominoes in the player's hand. Used when the game ends due to a blocked board.
        """
        return sum((domino.size() for domino in self.dominoes))

    def make_move(self):
        """
        Logic for making a move on the board. The current dummy logic simply select the first domino in the set that
        can be played on the current board configuration.
        Returns a tuple of the domino used, the side of the domino that matches, the side of the board to play it on,
         and the players completion status.
        """
        board = self.board
        if board.is_empty():
            domino = self.dominoes.pop()
            return (domino, 1, 'left')
        else:
            for domino in self.dominoes:
                if domino(1) == board('left'):
                    response = (domino, 1, 'left')
                    break
                elif domino(1) == board('right'):
                    response = (domino, 1, 'right')
                    break
                elif domino(2) == board('left'):
                    response = (domino, 2, 'left')
                    break
                elif domino(2) == board('right'):
                    response = (domino, 2, 'right')
                    break
            else:
                raise CannotPlay

            self.dominoes.remove(response[0])
            return response


class Game(object):

    def __init__(self, size, board, players):
        self.board = board
        self.player_set = players
        dominoes = self._create_domino_set(size)

        for player in self.player_set:
            for count in range(7):
                rand = randint(0, len(dominoes)-1)
                player.add_domino(dominoes.pop(rand))
            print("Player {}'s dominoes are {}".format(
                player.order, player.dominoes)
            )

    def _create_domino_set(self, size):
        dominoes = []
        for i in range(size + 1):
            for j in range(i, size + 1):
                dominoes.append(Domino(i, j))
        return dominoes

    def _end_via_block(self):
        final_score = [(player, player.add_remaining_dominoes()) for player in self.player_set]
        final_score.sort(key=lambda x: x[1])
        print("Player {} has won with {} points remaining!".format(final_score[-1][0].order, final_score[-1][1]))

    def _end_via_completion(self, player):
        print("Player {} has used all their dominoes! They are the winner!".format(player.order))

    def run(self):
        board = self.board
        skipped = 0
        running = True
        while running:
            for player in self.player_set:
                try:
                    domino, side, end = player.make_move()
                except CannotPlay:
                    print("Player {} skips their turn.".format(player.order))
                    skipped +=1
                    if skipped == 4:
                        self._end_via_block()
                        running = False
                        break
                else:
                    print("Player {} plays {}".format(player.order, domino))
                    time.sleep(2)
                    skipped = 0
                    board.update_board(domino, side, end)
                    if player.check_for_completion():
                        self._end_via_completion(player)
                        running = False
                        break


def run():
    max_size = 6  # config['DEFAULT_SIZE']

    board = Board()
    players = [Player(i, board) for i in range(1, 5)]
    game = Game(max_size, board, players)
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
        attempt = run()
    except KeyboardInterrupt:
        sys.exit(1)
    except SystemError:
        raise
    except:
        exc_info = sys.exc_info()
        exc_class, exc, tb = exc_info
        tb_path, tb_line_no, tb_func = traceback.extract_tb(tb)[-1][:3]
        raise
        # print(
        #     "{} ({}:{} in {}".format(
        #         exc_info[1], tb_path, tb_line_no, tb_func
        #     )
        # )
        # logger.error(
        #     "{} ({}:{} in {}".format(
        #         exc_info[1], tb_path, tb_line_no, tb_func
        #     )
        # )
    else:
        sys.exit(attempt)