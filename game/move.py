class Move:
    def __init__(self, start, end):
        self._start = start
        self._end = end

class InitialMove(Move):
    def __init__(self, cell):
        self._cell = cell