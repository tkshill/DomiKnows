__author__ = 'Kirk'

import app
import unittest
from unittest import mock

class TestDominoDominoes(unittest.TestCase):

    def setUp(self):
        self.domino = app.Domino(3, 4)

    def test_domino_returns_correct_size(self):
        self.assertEqual(7, self.domino.size())

    def test_sides_return_correct_value(self):
        self.assertEqual((3, 4), (self.domino.side_1, self.domino.side_2))

    def test_domino_string(self):
        self.assertEqual(self.domino.__str__(), self.domino.__repr__())

    def test_domino_call_returns_sides(self):
        self.assertEqual(4, self.domino(2))
        self.assertRaises(app.DominoArgValueError, self.domino, 'f')


class TestBoardMethods(unittest.TestCase):

    def setUp(self):
        self.b = app.Board()
        self.b2 = app.Board()
        self.d = app.Domino(4,6)
        self.d2 = app.Domino(6,0)

    def test_empty_board_verify(self):
        self.assertEqual(self.b.is_empty(), True)

    def test_call_method(self):
        self.assertRaises(IndexError, self.b2, 'left')
        self.b2.update_board(self.d, 2, 'right')
        self.assertEqual(self.b2('left'), 6)

    def test_call_with_bad_args(self):
        self.assertRaises(app.BoardArgValueError, self.b2.__call__, 'top')

    def test_add_domino_to_board(self):
        self.b.update_board(self.d, 1, 'right')
        self.assertEqual(self.b('left'), 4)

        self.b.update_board(self.d2, 1, 'right')
        self.assertEqual(self.b('right'), 0)


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




















