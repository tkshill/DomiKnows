__author__ = 'Kirk'

import app
import unittest
from unittest import mock


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        self.board = app.Board()
        self.player = app.Player(4, self.board)

    def test_add_domino(self):
        p = self.player
        d = app.Domino(4,7)
        p.add_domino(d)
        self.assertIn(d, p.dominoes)

    def test_check_for_completion(self):
        p = self.player
        self.assertEqual(p.check_for_completion(), True)
        d = app.Domino(5, 5)
        p.add_domino(d)
        self.assertEqual(p.check_for_completion(), False)

    def test_add_remaining_dominoes(self):
        p = self.player
        d = app.Domino(5, 5)
        d2 = app.Domino(2, 3)
        p.add_domino(d)
        p.add_domino(d2)
        self.assertEqual(p.add_remaining_dominoes(), 15)

    def test_make_move(self):
        board = self.board
        d = app.Domino(4,5)
        board.update_board(d, 1, 'right')

        d2 = app.Domino(3, 4)
        d3 = app.Domino(1, 6)
        self.player.add_domino(d2)
        self.player.add_domino(d3)

        domino, side, end = self.player.make_move()

        self.assertEqual(domino, d2)
        self.assertEqual(side, 2)
        self.assertEqual(end, 'left')

    def test_make_move_raises_error_if_no_match(self):
        board = self.board
        d = app.Domino(4,5)
        board.update_board(d, 1, 'right')

        d2 = app.Domino(0, 2)
        d3 = app.Domino(1, 6)
        self.player.add_domino(d2)
        self.player.add_domino(d3)

        self.assertRaises(app.CannotPlay, self.player.make_move)


class TestGame(unittest.TestCase):

    def setUp(self):

        size = 6
        self.g = app.Game(size)




















