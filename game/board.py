import enum
from .move import Move


# Board represented by double array of booleans (True = occupied, False = empty)
class Board:
    size = 18

    def __init__(self):
        self._board = [[True] * Board.size] * Board.size
    
    # Get a cell (occupied/not occupied) by index or coord
    def __getitem__(self, index):
        if index.__class__ == int:
            return self._board[index]
        if index.__class__ == tuple:
            return Cell(self, index, self._board[index[0]][index[1]])
        raise TypeError

    # Iterate all cells (only occupied, removed, or of a color)
    def cells(self, occupied_only=False, removed_only=False, color=None):
        assert not (occupied_only and removed_only)
        for row in range(Board.size):
            for col in range(Board.size):
                cell = Cell(self, (row, col), self._board[row][col])
                if occupied_only and not cell.occupied():
                    continue
                if removed_only and cell.occupied():
                    continue
                if color is not None and cell.color() != color:
                    continue
                yield cell

    def n_occupied(self):
        return sum(sum(row) for row in self._board)
    
    def n_removed(self):
        return (Board.size ** 2) - self.n_occupied()

    # Generates/returns new board after applying move
    def __add__(self, next_move):
        assert isinstance(next_move, Move)
        next_board = Board()
        next_board._board = [row[:] for row in self._board]
        for piece in next_move.added():
            next_board._board[piece.row()][piece.col()] = True
        for piece in next_move.removed():
            next_board._board[piece.row()][piece.col()] = False
        return next_board
    
    def __str__(self):
        cells = [['-'] * Board.size for _ in range(Board.size)]
        for c in self.cells(occupied_only=True):
            cells[c.row()][c.col()] = {
                Color.white: '□',
                Color.black: '■',
                Color.nocolor: '?'
            }[c.color()]
        return '\n'.join(f'{idx+1:>2} ' + ' '.join(row) for (idx, row) in reversed(list(enumerate(cells)))) + '\n-- ' + ' '.join(chr(c) for c in range(97, 97+Board.size))


# Cell has reference to its board, (x, y) coords, and bool
class Cell:
    def __init__(self, board, coord, occupied):
        (self._row, self._col) = coord
        self._board = board
        self._occupied = occupied

    def color(self):
        return Color.white if (self._row + self._col) % 2 == 0 else Color.black

    def occupied(self):
        return self._occupied

    def coord(self):
        return self._row, self._col

    def row(self):
        return self._row
    
    def col(self):
        return self._col

    def neighbor(self, v_row, v_col):
        if not Cell.valid(self._row + v_row, self._col + v_col):
            raise IndexError
        return self._board[(self._row + v_row, self._col + v_col)]
    
    # Returns captured cell
    def __add__(self, direction):
        return self.neighbor(*direction)
    
    def __sub__(self, other):
        return self._row - other._row, self._col - other._col

    def __str__(self):
        return f'({self._row + 1}, {chr(self._col + 97)})'
    
    @classmethod
    def valid(cls, row, col):
        return (0 <= row < Board.size) and (0 <= col < Board.size)


class Color(enum.IntEnum):
    white = 0
    black = 1
    nocolor = 2


class Direction(enum.Enum):
    left = (0, -1)
    right = (0, +1)
    up = (+1, 0)
    down = (-1, 0)