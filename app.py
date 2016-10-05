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


class Player(object):
    """
    Player represents exactly what you think. Each player has a set of dominoes, a game which they are a part of
    (and thus access to viewing the game's board). Players can make moves and (eventually) analyze the board to make the
    best moves.
    """
    def __init__(self, order):
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
        return sum([d[0] + d[1] for d in self.dominoes])

    def decide_move(self, board):
        """
        Logic for making a move on the board. The current dummy logic simply select the first domino in the set that
        can be played on the current board configuration.
        Returns a tuple of the domino used, the side of the domino that matches, the side of the board to play it on,
         and the players completion status.
        """
        if not board:
            domino = self.dominoes.pop()
            return self._move('appendleft', domino[0], domino[1])

        else:
            for domino in self.dominoes:

                if domino[0] == board[0][0]:
                    self.dominoes.remove(domino)
                    return self._move('appendleft', domino[1], domino[0])

                elif domino[0] == board[-1][-1]:
                    self.dominoes.remove(domino)
                    return self._move('append', domino[0], domino[1])

                elif domino[1] == board[0][0]:
                    self.dominoes.remove(domino)
                    return self._move('appendleft', domino[0], domino[1])

                elif domino[1] == board[-1][-1]:
                    self.dominoes.remove(domino)
                    return self._move('append', domino[1], domino[0])

            else:
                raise CannotPlay

    def _move(self, method, val_1, val_2):
        def call_board_action(container):
            action = getattr(container, method)
            action((val_1, val_2))

        return call_board_action


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
                dominoes.append((i, j))
        return dominoes

    def _end_via_block(self):
        final_result = [(player, player.add_remaining_dominoes()) for player in self.player_set]
        final_result.sort(key=lambda x: x[1])
        print("Player {} has won with {} points remaining!".format(final_result[-1][0].order, final_result[-1][1]))

    def _end_via_completion(self, player):
        print("Player {} has used all their dominoes! They are the winner!".format(player.order))

    def run(self):
        board = self.board
        skipped = 0
        running = True
        while running:
            for player in self.player_set:
                print(board)
                try:
                    decision = player.decide_move(board)
                except CannotPlay:
                    print("Player {} skips their turn.".format(player.order))
                    skipped +=1
                    if skipped == 4:
                        self._end_via_block()
                        running = False
                        break
                else:
                    time.sleep(1)
                    print("Player {} makes a move!".format(player.order))
                    skipped = 0
                    decision(board)
                    if player.check_for_completion():
                        self._end_via_completion(player)
                        running = False
                        break


def run():
    max_size = 6  # config['DEFAULT_SIZE']
    board = deque()
    players = [Player(i) for i in range(1, 5)]
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