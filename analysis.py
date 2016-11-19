__author__ = 'Kirk'

import collections
import app
import matplotlib.pyplot as plt


def fake_print(*args):
    pass


def create_players(num):
    return [app.Player(x) for x in range(1, num+1)]


def assemble_game():
    players = create_players(4)
    dominoes = app.create_domino_set(6)
    app.assign_dominoes(dominoes, players)
    return app.Game(app.deque(), players)


if __name__ == "__main__":

    app.print = fake_print

    fig, ax = plt.subplots()

    results = collections.Counter([assemble_game().run() for _ in range(10000)])

    xlabels, values = [(i, results[i]) for i in results]
    print(results)



