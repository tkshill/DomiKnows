__author__ = 'Kirk'
__version__ = 0.1

"""
Sample application to implement a version of the dominoes game in python. Also
an attempt by the creator to explore machine learning, application development,
version control, and PYTHON 3
"""

import sys
import configparser
import pathlib
import logging
from random import randint
from collections import deque
import traceback
import time

CONFIG_NAME = "default_config.cfg"
LOGGING_FILE = "domi_knows.log"

config = configparser.ConfigParser()
logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)


# def fake_print(*args):
#     return None

def string_to_bool(s):
    return str(s).lower() in ("yes", "true", "t", "1")


def make_config_file(config_name):
    config["DEFAULT"] = {"MAX_DOMINO": "6",
                         "HUMAN_PLAYER": "False",
                         "PLAYER_NUM": "4",
                         "DEBUG_MODE": "True",
                         # "PRINT_SUPPRESS": "True",
                         }

    with open(config_name, "w") as configfile:
        config.write(configfile)


def flip(domino):
    """
    Accepts a non-empty tuple and returns it with first and last parameters
    reversed. Used in this app to flip tuples representing dominoes.
    """
    return (domino[1], domino[0])


def create_domino_set(size):
    """
    Accepts an integer for the highest number to be printed on a domino.
    Returns a set of dominoes of size ( (n**2 + 3n)/2 ) + 1 where n is the
    size passed in. Each domino is a tuple containing two values each where
    0 <= value <= size.
    """
    dominoes = []
    for i in range(size + 1):
        for j in range(i, size + 1):
            dominoes.append((i, j))
    return dominoes


def assign_dominoes(dominoes, players):
    """
    Accepts a set of dominoes and a list of players. Places a random domino
    in the set to players in sequence.
    """
    hand_number = int(len(dominoes)/len(players))

    for player in players:
        for count in range(hand_number):
            rand = randint(0, len(dominoes)-1)
            player.add_domino(dominoes.pop(rand))


def make_players(num):
    if num >= 1:
        return [Player(i) for i  in range(1, num + 1)]
    else:
        raise IndexError("Number must be greater than 0")

class MyException(Exception):
    """
    Base class for custom exceptions.
    """
    pass


class CannotPlay(MyException):
    """
    Custom Exception Cannot Play when the player's dominoes match up to no
    dominoes on the board.
    """
    pass


class PlayerQuit(MyException):
    """
    Player chooses to end game
    """


class Player(object):
    """
    Player represents exactly what you think. Each player has a set of
    dominoes. Players can make moves and (eventually) analyze the board
    to make the best moves.
    """
    def __init__(self, order):
        self.order = order
        self.dominoes = []

    def add_domino(self, domino):
        """
        Adds a single domino tuple to the set of dominoes.
        """
        self.dominoes.append(domino)

    def check_for_completion(self):
        """
        Checks if player has played all the dominoes given at the start of the
        game/Checks if their dominoes_set is empty. Returns True or False
        """
        return False if self.dominoes else True

    def add_remaining_dominoes(self):
        """
        Returns the sum of the remaining dominoes in the player's hand. Used
        when the game ends due to a blocked board.
        """
        return sum([d[0] + d[1] for d in self.dominoes])

    def decide_move(self, board):
        """
        Logic for making a move on the board. The current dummy logic simply
        select the first domino in the set that can be played on the current
        board configuration.
        Returns a tuple of the domino used, the side of the domino that
        matches, the side of the board to play it on, and the players
        completion status.
        """

        # if board has no dominoes yet
        if not board:
            domino = self.dominoes.pop()

            # nothing special about this particular configuration.
            return self._move('appendleft', domino)

        else:
            left_end = board[0][0]
            right_end = board[-1][-1]

            # iterate through each domino in hand, checking for a match with a
            # side of the board.
            for domino in self.dominoes:

                if domino[0] == left_end:
                    self.dominoes.remove(domino)
                    return self._move('appendleft', flip(domino))

                elif domino[0] == right_end:
                    self.dominoes.remove(domino)
                    return self._move('append', domino)

                elif domino[1] == left_end:
                    self.dominoes.remove(domino)
                    return self._move('appendleft', domino)

                elif domino[1] == right_end:
                    self.dominoes.remove(domino)
                    return self._move('append', flip(domino))

            else:
                # if the player goes through all their dominoes without finding
                # a match with the board, raise error
                raise CannotPlay

    def _move(self, method, domino):
        """
        Accepts a string representing deque methods 'append' or 'appendleft'
        and the two sides of the domino to be placed on the board.

        Uses a closure to Return a Function that will accept a deque (board),
        bind the appropriate board method to a name, and call that method with
        a tuple representing the domino to be played.

        e.g.
        >>> p = Player(1)
        >>> decision = p._move('append', (4, 5))
        >>> b = deque()
        >>> b
        deque([])
        >>> decision(b)
        >>>b
        deque([(4, 5)])
        """
        def call_board_action(container):
            action = getattr(container, method)
            action(domino)

        return call_board_action


class HumanPlayer(Player):

    def __init__(self, order):
        super().__init__(order)

    def decide_move(self, board):
        print(
            "\nSelect the number of the domino you wish to play. ",
            "followed by a space, and then either 'left' or 'right'.\n",
            "enter 'skip' to skip your turn or 'quit' to exit game.\n"
        )

        for inc, domino in enumerate(self.dominoes):
            print("{}: {}".format(inc + 1, domino))

        playing = True
        while playing:
            response = input("Enter answer here.")

            if response == "skip":
                raise CannotPlay

            if response == "quit":
                print("Thanks for trying out DomiKnows")
                sys.exit(0)

            response = response.split(" ")

            try:
                num = response[0]
                side = response[1]
            except IndexError:
                print("Invalid answer format. Please try again.")
                continue

            try:
                domino = self.dominoes[int(num) - 1]
            except IndexError:
                print("The domino position you've entered is invalid. \n",
                      "Please try again.")
                continue

            except ValueError:
                print("The domino position you've entered is invalid. \n",
                      "Please try again.")
                continue

            if side not in ("left", "right"):
                print("Invalid side. Please select either 'left' or 'right'.")
                continue

            left_end = board[0][0]
            right_end = board[-1][-1]

            if side == "left":
                if domino[0] == left_end:
                    self.dominoes.remove(domino)
                    return self._move('appendleft', flip(domino))

                elif domino[1] == left_end:
                    self.dominoes.remove(domino)
                    return self._move('appendleft', domino)
                else:
                    print("The domino you chose cannot be played in that location.")

            elif side == "right":
                if domino[0] == right_end:
                    self.dominoes.remove(domino)
                    return self._move('append', domino)

                elif domino[1] == right_end:
                    self.dominoes.remove(domino)
                    return self._move('append', flip(domino))
                else:
                    print("The domino you chose cannot be played in that location.")

            else:
                print("The domino you chose cannot be played in that location.")


class Game(object):
    """
    Object representing the data and logic necessary to play a single game of
    dominoes.
    """

    def __init__(self, board, players):
        self.board = board  # deque which dominoes will be played on
        self.player_set = players

    def _end_via_block(self):
        """
        Prints the player with the lowest valued set of dominoes in the case
        that no one can play.
        """

        # List of each player's number and the sum of their remaining dominoes.
        final_result = [
            (player, player.add_remaining_dominoes())
            for player in self.player_set
            ]

        # sort via the sum in ascending order
        final_result.sort(key=lambda x: x[1])
        winner = final_result[0][0]
        points = final_result[0][1]

        return self._end(winner, "has finished with {} points remaining".format(points))

    def _end(self, player, message):
        """
        Accepts player who finished their hand first and prints their success.
        """
        print(" ".join(("Player {}".format(player.order), message)))
        return player.order

    def run(self):
        """
        Driving logic for a single game. A loop drives each player to make a
        move based on the board, and updates that board based on the players'
        moves.
        """
        board = self.board
        skipped = 0
        running = True

        while running:
            for player in self.player_set:
                try:
                    # attempt to get a valid move from the player
                    decision = player.decide_move(board)
                except CannotPlay:
                    # players raise an error if they cannot make a move.
                    print("Player {} skips their turn.".format(player.order))

                    skipped += 1

                    # if skipped counter hits four then that means every player
                    # has skipped a turn in sequence.
                    # so the board is blocked on both ends.
                    if skipped == 4:
                        return self._end_via_block()

                else:
                    time.sleep(0.5)  # for the purpose of observation
                    skipped = 0  # reset the skipped turn counter

                    # apply the player's decision to the board
                    decision(board)
                    print("{}: {}".format(player.order, board))
                    # if the player has no more dominoes left...
                    if player.check_for_completion():
                        return self._end(
                            player, "has finished all their dominoes!")


def run():
    """
    Initiation point. Creates all the objects necessary for a game.
    """
    num_players = int(config["DEFAULT"]["PLAYER_NUM"])
    max_domino = int(config["DEFAULT"]["MAX_DOMINO"])
    with_human = string_to_bool(config["DEFAULT"]["HUMAN_PLAYER"])

    # if string_to_bool(config["DEFAULT"]["PRINT_SUPPRESS"]):
    #     print = fake_print

    if with_human:
        players = make_players(num_players-1)
        hp = HumanPlayer(4)
        players.append(hp)
    else:
        players = make_players(num_players)

    dominoes = create_domino_set(max_domino)
    board = deque()  # game 'board'
    assign_dominoes(dominoes, players)

    game = Game(board, players)  # initialize a game instance
    game.run()


if __name__ == "__main__":

    if not pathlib.Path(CONFIG_NAME).is_file():
        make_config_file(CONFIG_NAME)
    else:
        config.read(CONFIG_NAME)

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
        if bool(config["DEFAULT"]['DEBUG_MODE']):
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