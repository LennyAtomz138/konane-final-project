from .board import (Board, Color, Direction)
from .move import (Move, InitialMove)


# Maintains a game state, i.e. a snapshot of the game in time
# Contains a board state and the color of the current player.
# Get a generator of available moves with State#moves()
class State:
    def __init__(self, board, color=Color.nocolor):
        self._board = board
        self._color = color

    def board(self):
        return self._board

    def color(self):
        return self._color
    
    def is_loss(self):
        return next(self.moves(), None) is None

    def moves(self):
        if self._board.n_removed() == 0:
            return self._firstmove()
        if self._board.n_removed() == 1:
            return self._secondmove()
        return self._moves()

    def __add__(self, next_move):
        c = self._color
        if self._color == Color.nocolor:
            assert isinstance(next_move, InitialMove)
            c = next_move.removed()[0].color()
        next_color = (Color.white if c == Color.black else Color.black)
        return State(self._board + next_move, next_color)

    def _firstmove(self):
        a = 0
        b = Board.size-1
        c = Board.size // 2
        d = c - 1
        candidates = [
            (a, a), (a, b), (b, a), (b, b),
            (c, c), (c, d), (d, c), (d, d)
        ]
        for cell in candidates:
            yield InitialMove(self._board[cell])

    def _secondmove(self):
        hole = list(self._board.cells(removed_only=True))[0]
        for direction in Direction:
            try:
                yield InitialMove(hole + direction.value)
            except IndexError:
                pass
    
    # Generates all valid moves current color can make
    def _moves(self):
        for cell in self._board.cells(occupied_only=True, color=self._color):
            for direction in Direction:
                direction = direction.value
                ptr = cell
                try:  # Can capture a piece
                    while (ptr + direction).occupied() and not (ptr + direction + direction).occupied():
                        destination = ptr + direction + direction
                        yield Move(cell, destination)
                        ptr = destination # Consecutive jumps are separate moves
                except IndexError:  # Move OOB
                    pass

    # Efficient counter of # of moves for Mobility term
    def numMoves(self):
        count = 0
        for cell in self._board.cells(occupied_only=True, color=self._color):
            for direction in Direction:
                direction = direction.value
                ptr = cell
                try: 
                    while (ptr + direction).occupied() and not (ptr + direction + direction).occupied():
                        destination = ptr + direction + direction
                        ptr = destination  # Consecutive jumps are separate moves
                except IndexError:
                    pass
        return count
    
    def __str__(self):
        return f'{self._board}\n{self._color.name}'
