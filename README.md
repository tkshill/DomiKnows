# DomiKnows
Python plays dominoes! A small application that currently has four non-human "players" engaging in a game of Dominoes. Plans to expand into an interactive game with human players, with some machine learning for the computer opponents! Please take a look!

#Installation
N/A

#Usage Example
N/A

#Development Setup
N/A

#Release History
N/A

#What are dominoes?

A simple description, taken from wikipedia:

"Dominoes (or dominos) is a game played with rectangular "domino" tiles. The domino gaming pieces make up a domino set, sometimes called a deck or pack. The traditional Sino-European domino set consists of 28 dominoes, colloquially nicknamed bones, cards, tiles, tickets, stones, or spinners. Each domino is a rectangular tile with a line dividing its face into two square ends. Each end is marked with a number of spots (also called pips, nips, or dobs) or is blank. The backs of the dominoes in a set are indistinguishable, either blank or having some common design. A domino set is a generic gaming device, similar to playing cards or dice, in that a variety of games can be played with a set.

...

The most basic domino variant is for two players and requires a double-six set. The 28 tiles are shuffled face down and form the stock or boneyard. Each player draws seven tiles; the remainder are not used. Once the players begin drawing tiles, they are typically placed on-edge before the players, so each player can see his own tiles, but none can see the value of other players' tiles. Every player can thus see how many tiles remain in the other players' hands at all times during gameplay. One player begins by downing (playing the first tile) one of their tiles. This tile starts the line of play, a series of tiles in which adjacent tiles touch with matching values. The players alternately extend the line of play with one tile at one of its two ends. The game ends when one player wins by playing their last tile, or when the game is blocked because neither player can play. If that occurs, whoever caused the block gets all of the remaining player points not counting their own."

#Why dominoes?

Dominoes is uniquely suited to this type of experimental application for the following reasons:

1. The base logic of dominoes is extremey simple. EXTREMELY. One of the reasons why the game is so popular is how quickly it be taught. If you have the ability to count and recognize the numbers between 0 and 10, you can execute the game. This made it a great candidate for a game to make for someone like me, who has little experience implementing real-world game logic in a programming environment. Easy to learn, but hard to master seemed like the ideal candidate for machine learning.

2. Dominoes is partially a game of chance. The hand dealt to each player at the beginning of the game is (mostly) randomized, making each game configuration essentially unique with ~ 1.18 million unique hands for any given player and 4.7 e14 starting game configurations for the standard four person game. This makes it great for doing statistical analysis with high populations. 

3. Dominoes is ultimately, a logic game. After the initial phase of random matching of tiles, game players move to higher levels of play where move determination takes into considering:

- the tiles the player currently possesses
- the state of the board at the time of play
- the moves played by the Other players and the sequence they were played in

4. Most importantly, I love dominoes. In my country, the game is extremely popular, more so than any other board or card game. I myself have played hundreds of hours of dominoes and will almost never pass up an opportunity to do so. 

#Meta
Kirk Shillingford - tkshillingford@gmail.com
