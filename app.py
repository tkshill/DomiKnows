__author__ = 'Kirk'
__version__ = 0.1

"""
Sample application to implement a version of the dominoes game in python. Also an attempt by the creator to explore
machine learning, application development, version control, and PYTHON 3
"""

import sys
import configparser
import pathlib
from random import randint
from collections import deque

config = configparser.ConfigParser()
CONFIG_NAME = 'default_config.cfg'

# TODO remove the ends attribute in boards and just reference the ends of the deques
# TODO add logic for how to determine move when not playing first
# TODO write doctests/unittests for all available methods
# TODO subclass player to make human player
# TODO add command line arguments so game can be started with 4 comp players or 3 comp one human player
# TODO GUI/NO GUI? Kivy or tkinter
# TODO Machine learnin'

class CannotPlay(Exception):
    """
    Custom Exception Cannot Play when the player's dominoes match up to no dominoes on the board
    """
    pass


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
        of side 2. Mainly to expedite checking whether a domino matches ends without having to refer to side1 and side2.
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
    Represents a game board. Each game has one. Players can inspect tiles on board. Dominoes are transferred from the
    players to the board.
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
    """
    Player represents exactly what you think. Each player has a set of dominoes, a game which they are a part of
    (and thus access to viewing the game's board). Players can make moves and (eventually) analyze the board to make the
    best moves.
    """
    def __init__(self, order, game):
        self.board = game.board
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
                else:
                    raise CannotPlay


class Game(object):

    def __init__(self, size):
        self.board = Board()
        self.player_set = [Player(order, self) for order in range(1, 5)]

        dominoes = self._create_domino_set(size)

        for player in self.player_set:
            for count in range(7):
                rand = randint(0, len(dominoes)-1)
                player.add_domino(dominoes.pop(rand))

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
        final_score = [(player, player.add_remaining_dominoes()) for player in self.player_set]
        final_score.sort(key=lambda x: x[1])
        print("Player {} has won with {} points remaining!".format(final_score[-1][0].order, final_score[-1][1]))

    def end_via_completion(self, player):
        print("Player {} has used all their dominoes! They are the winner!".format(player.order))

    def run(self):
        board = self.board
        skipped = 0
        running = True
        while running:
            for player in self.player_set:
                try:
                    domino, side, end, win_status = player.make_move()
                    skipped = 0
                except CannotPlay:
                    skipped +=1
                    if skipped == 4:
                        self.end_via_block()
                        running = False
                else:
                    board.update_board(domino, side, end)
                    if win_status:
                        self.end_via_completion(player)
                        running = False



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