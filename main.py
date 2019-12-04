from game.player import HumanPlayer
from game.game import Game

if __name__ == '__main__':
    p0 = HumanPlayer('Player 0')
    p1 = HumanPlayer('Player 1')
    g = Game(p0, p1)
    winner = g.run_all()
    print(winner)