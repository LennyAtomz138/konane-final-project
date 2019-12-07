from .board import Board
from .state import State


# Game#run_all() causes players to make moves until game over. Returns winning player
class Game:
    def __init__(self, p0, p1):
        self._p = [p0, p1]
        self._state = State(Board())
        self._player = 0

    def __iter__(self):
        while not self._state.is_loss():
            move = self._p[self._player].next_move(self._state)
            yield move
            self._state = self._state + move
            self._player = [1,0][self._player]

    def player(self, index):
        return self._p[index]

    def state(self):
        return self._state
    
    def current(self):
        return self._player

    def loser(self):
        assert self._state.is_loss()
        return self._player

    def winner(self):
        assert self._state.is_loss()
        return [1,0][self._player]

    def run_all(self):
        for _ in self:
            pass
        return self.player(self.winner())