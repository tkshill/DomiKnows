__author__ = 'Kirk'

import app
import unittest


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        self.board = app.deque()
        self.player = app.Player(4)

    def test_add_domino(self):
        p = self.player
        d = (4, 7)
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
        d = (4, 5)
        board.append(d)

        d2 = (3, 4)
        d3 = (1, 6)
        self.player.add_domino(d2)
        self.player.add_domino(d3)

        decision = self.player.decide_move(board)
        decision(board)

        self.assertEqual(board, app.deque(((3, 4), (4, 5))))

    def test_make_move_raises_error_if_no_match(self):
        board = self.board
        d = (4, 5)
        board.append(d)

        d2 = (0, 2)
        d3 = (1, 6)
        self.player.add_domino(d2)
        self.player.add_domino(d3)

        self.assertRaises(app.CannotPlay, self.player.decide_move, board)


class TestSupportFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_dominoes(self):
        dominoes = app.create_domino_set(6)
        self.assertEqual(len(dominoes), 28)

        dominoes2 = app.create_domino_set(7)
        self.assertEqual(len(dominoes2), 36)

        dominoes3 = app.create_domino_set(0)
        self.assertEqual(len(dominoes3), 1)

    def test_domino_assignment(self):

        dominoes = app.create_domino_set(6)
        players = app.make_players(4)

        dominoes2 = app.create_domino_set(7)
        players2 = app.make_players(6)

        app.assign_dominoes(dominoes, players)
        self.assertEqual(7, len(players[1].dominoes))

        app.assign_dominoes(dominoes2, players2)
        self.assertEqual(6, len(players2[2].dominoes))


class TestPlayerSubClass(unittest.TestCase):

    def test_player_can_choose_move(self):

        def fake_input(*args):
            return("1 left")

        app.input = fake_input
        human = app.HumanPlayer(4)
        human.dominoes = [(4, 5)]

        b = app.deque()
        b.append((5, 6))

        move = human.decide_move(b)
        move(b)
        self.assertEqual(b[0], (4, 5))


class TestObjectCreation(unittest.TestCase):

    def test_domino_amount(self):
        self.assertEqual(28, len(app.create_domino_set(6)))
        self.assertEqual(6, len(app.create_domino_set(2)))
        self.assertEqual(1, len(app.create_domino_set(0)))


    def test_player_creation(self):
        self.assertEqual(5, len(app.make_players(5)))
        self.assertRaises(IndexError, app.make_players, -2)


class TestGame(unittest.TestCase):

    def test_game_returns_integer(self):
        ds = app.create_domino_set(6)
        ps = app.make_players(4)
        app.assign_dominoes(ds, ps)
        g = app.Game(app.deque(), ps)

        self.assertIsInstance(g.run(), int)

    def test_endings(self):
        g = app.Game(None, None)
        p = app.Player(1)

        self.assertEqual(1 ,g._end(p, "is an idiot"))

        p2 = app.Player(2)

        p.add_domino((6, 6))
        p2.add_domino((2, 3))

        g.__init__(app.deque(), [p, p2])

        self.assertEqual(2, g._end_via_block())


class TestDataAnalysis(unittest.TestCase):
    pass



