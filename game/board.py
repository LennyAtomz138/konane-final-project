import enum
import move

class Board:
    __size = 18

    def __init__(self):
        self._board = [[True] * Board.__size] * Board.__size
    
    def __getitem__(self, index):
        if index.__class__ == int:
            return self._board[index]
        if index.__class__ == tuple:
            return Cell(self, index, self._board[index[0]][index[1]])
        raise TypeError

    def cells(self, occupied_only=False, removed_only=False, color=Color.nocolor):
        assert not (occupied_only and removed_only)
        for row in range(Board.__size):
            for col in range(Board.__size):
                cell = Cell(self, (row, col), self._board[row][col])
                if occupied_only and not cell.occupied():
                    continue
                if removed_only and cell.occupied():
                    continue
                if color != Color.nocolor and cell.color() != color:
                    continue
                yield cell

    def n_occupied(self):
        return sum(sum(row) for row in self._board)
    
    def n_removed(self):
        return (Board.__size ** 2) - self.n_occupied()

    def __add__(self, next_move):
        assert isinstance(next_move, move.Move)
        next_board = Board()
        next_board._board = [row[:] for row in self._board]
        for piece in next_move.added():
            next_board._board[piece.row()][piece.col()] = True
        for piece in next_move.removed():
            next_board._board[piece.row()][piece.col()] = False
        return next_board
    
    def __str__(self):
        cells = [['-'] * Board.__size] * Board.__size
        for c in self.cells(occupied_only=True):
            cells[c.row()][c.col()] = {
                Color.white: 'X',
                Color.black: 'O',
                Color.nocolor: '?'
            }[c.color()]
        return '\n'.join(' '.join(row) for row in cells)

class Cell:
    def __init__(self, board, coord, occupied):
        (self._row, self._col) = coord
        self._board = board
        self._occupied = occupied

    def color(self):
        return (Color.white if (self._row + self._col) % 2 == 0 else Color.black)

    def occupied(self):
        return self._occupied

    def coord(self):
        return (self._row, self._col)

    def row(self):
        return self._row
    
    def col(self):
        return self._col

    def neighbor(self, v_row, v_col):
        if not Cell.valid(self._row + v_row, self._col + v_col):
            raise IndexError
        return self._board[(self._row + v_row, self._col + v_col)]
    
    def __add__(self, direction):
        return self.neighbor(*direction)
    
    def __sub__(self, other):
        return (self._row - other._row, self._col - other._col)

    def __str__(self):
        return f'({self._row + 1}, {chr(self._col + ord('a'))})'
    
    @classmethod
    def valid(cls, row, col):
        return (0 <= row < Board.__size) and (0 <= col < Board.__size)

class Color(enum.IntEnum):
    white = 0
    black = 1
    nocolor = 2

class Direction(enum.Enum):
    left = (0, -1)
    right = (0, +1)
    up = (+1, 0)
    down = (-1, 0)