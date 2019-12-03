import board
from board import Board
from move import (Move, InitialMove)

# Maintains a game state, i.e. a snapshot of the game in time
# Contains a board state and the color of the current player.
# Get a generator of available moves with State#moves()
class State:
    def __init__(self, board, color):
        self._board = board
        self._color = color

    def board(self):
        return self._board

    def color(self):
        return self._color
    
    def is_loss(self):
        return next(self.moves(), None) == None

    def moves(self):
        if self._board.n_removed() == 0:
            return self._firstmove()
        if self._board.n_removed() == 1:
            return self._secondmove()
        return self._moves()
    
    def _firstmove(self):
        a = 0
        b = Board.__size-1
        c = Board.__size / 2
        d = c - 1
        candidates = [
            (a,a), (a,b), (b,a), (b,b),
            (c,c), (c,d), (d,c), (d,d)
        ]
        for cell in candidates:
            yield InitialMove(self._board[cell])

    def _secondmove(self):
        hole = [self._board.cells(removed_only=True)][0]
        for direction in board.Direction:
            try:
                yield InitialMove(hole + direction)
            except IndexError:
                pass

    def _moves(self):
        for cell in self._board.cells(occupied_only=True, color=self._color):
            for direction in board.Direction:
                ptr = cell
                try:
                    while (ptr + direction).occupied() and not (ptr + direction + direction).occupied():
                        destination = ptr + direction + direction
                        yield Move(cell, destination)
                        ptr = destination
                except IndexError:
                    pass