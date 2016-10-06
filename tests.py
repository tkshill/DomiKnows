__author__ = 'Kirk'

import app
import unittest
from unittest import mock


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        self.board = app.deque()
        self.player = app.Player(4)

    def test_add_domino(self):
        p = self.player
        d = (4,7)
        p.add_domino(d)
        self.assertIn(d, p.dominoes)

    def test_check_for_completion(self):
        p = self.player
        self.assertEqual(p.check_for_completion(), True)
        d = (5, 5)
        p.add_domino(d)
        self.assertEqual(p.check_for_completion(), False)

    def test_add_remaining_dominoes(self):
        p = self.player
        d = (5, 5)
        d2 = (2, 3)
        p.add_domino(d)
        p.add_domino(d2)
        self.assertEqual(p.add_remaining_dominoes(), 15)

    def test_make_move(self):
        board = self.board
        d = (4,5)
        board.append(d)

        d2 = (3, 4)
        d3 = (1, 6)
        self.player.add_domino(d2)
        self.player.add_domino(d3)

        decision = self.player.decide_move(board)
        decision(board)

        self.assertEqual(board, app.deque(((3,4), (4, 5))))

    def test_make_move_raises_error_if_no_match(self):
        board = self.board
        d = (4,5)
        board.append(d)

        d2 = (0, 2)
        d3 = (1, 6)
        self.player.add_domino(d2)
        self.player.add_domino(d3)

        self.assertRaises(app.CannotPlay, self.player.decide_move, board)


class TestGame(unittest.TestCase):

    def setUp(self):

        size = 6
        self.g = app.Game(size)




















