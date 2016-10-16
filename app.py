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
import time

config = configparser.ConfigParser()
CONFIG_NAME = 'default_config.cfg'
LOGGING_FILE = 'domi_knows.log'
DEBUG_MODE = True

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)


class MyException(Exception):
    """
    Base class for custom exceptions.
    """
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
        Adds a single domino tuple to the set of dominoes.
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

        # if board has no dominoes yet
        if not board:
            domino = self.dominoes.pop()

            # nothing special about this particular configuration.
            return self._move('appendleft', domino[0], domino[1])

        else:

            # iterate through each domino in hand, checking for a match with a side of the board.
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
                # if the player goes through all their dominoes without finding a match with the board, raise error
                raise CannotPlay

    def _move(self, method, val_1, val_2):
        """
        Accepts a string representing the deque methods 'append' or 'appendleft'
        and the two sides of the domino to be placed on the board.

        Uses a closure to Return a Function that will accept a deque (board), bind
        the appropriate board
        method to a name, and call that method with a tuple representing the domino to be played.

        e.g.
        >>> p = Player(1)
        >>> decision = p._move('append', 4, 5)
        >>> b = deque()
        >>> b
        deque([])
        >>> decision(b)
        >>>b
        deque([(4, 5)])
        """
        def call_board_action(container):
            action = getattr(container, method)
            action((val_1, val_2))

        return call_board_action


class Game(object):
    """
    Object representing the data and logic necessary to play a single game of dominoes.
    """

    def __init__(self, size, board, players):
        self.board = board  # deque which dominoes will be played on
        self.player_set = players
        dominoes = self._create_domino_set(size)
        self._assign_dominoes(dominoes, self.player_set)

    def _assign_dominoes(self, dominoes, players):
        """
        Accepts a set of dominoes and a list of players. Places a random domino in the set to players in sequence.
        """
        for player in players:
            for count in range(7):
                rand = randint(0, len(dominoes)-1)
                player.add_domino(dominoes.pop(rand))
            print("Player {}'s dominoes are {}".format(
                player.order, player.dominoes)
            )

    def _create_domino_set(self, size):
        """
        Accepts an integer for the highest number to be printed on a domino.
        Returns a set of dominoes of size ( (n**2 + 3n)/2 ) + 1 where n is the size passed in. Each domino is
        a tuple containing two values each where 0 <= value <= size.
        """
        dominoes = []
        for i in range(size + 1):
            for j in range(i, size + 1):
                dominoes.append((i, j))
        return dominoes

    def _end_via_block(self):
        """
        Prints the player with the lowest valued set of dominoes in the case that no one can play.
        """

        # create a list of each player's number and the sum of their remaining dominoes.
        final_result = [(player.order, player.add_remaining_dominoes()) for player in self.player_set]

        # sort via the sum in ascending order
        final_result.sort(key=lambda x: x[1])
        print(final_result)

        print("Player {} has won with {} points remaining!".format(final_result[-1][0], final_result[-1][1]))

    def _end_via_completion(self, player):
        """
        Accepts the player who finished their hand first and prints their success.
        """
        print("Player {} has used all their dominoes! They are the winner!".format(player.order))

    def run(self):
        """
        Driving logic for a single game. A loop drives each player to make a move based on the board,
        and updates that board based on the players' moves.
        """
        board = self.board
        skipped = 0
        running = True

        while running:
            for player in self.player_set:
                print(board)
                try:
                    # attempt to get a valid move from the player
                    decision = player.decide_move(board)
                except CannotPlay:
                    # players raise an error if they cannot make a move.
                    print("Player {} skips their turn.".format(player.order))

                    skipped +=1

                    # if skipped counter hits four then that means every player has skipped a turn in sequence.
                    # so the board is blocked on both ends.
                    if skipped == 4:
                        self._end_via_block()

                        # escape the for loop and halt the while loop. halt the for and escape the while?
                        running = False
                        break
                else:
                    time.sleep(3)  # for the purpose of observing the function running
                    print("Player {} makes a move!".format(player.order))
                    skipped = 0  # reset the skipped turn counter

                    # apply the player's decision to the board
                    decision(board)

                    # if the player has no more dominoes left...
                    if player.check_for_completion():
                        self._end_via_completion(player)
                        running = False
                        break


def run():
    max_size = 6  # config['DEFAULT_SIZE']
    board = deque()  # game 'board'
    players = [Player(i) for i in range(1, 5)]  # create four players
    game = Game(max_size, board, players)  # initialize a game instance
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
        # attempt normal execution
        attempt = run()

    # allow keyboard interrupts
    except KeyboardInterrupt:
        sys.exit(1)

    # do not log system level errors
    except SystemError:
        raise
    except:
        # log or print errors depending on development or not
        if DEBUG_MODE:
            raise
        else:
            exc_info = sys.exc_info()
            exc_class, exc, tb = exc_info
            tb_path, tb_line_no, tb_func = traceback.extract_tb(tb)[-1][:3]

            logger.error(
                "{} ({}:{} in {}".format(
                    exc_info[1], tb_path, tb_line_no, tb_func
                )
            )
    else:
        # graceful exit...
        sys.exit(attempt)