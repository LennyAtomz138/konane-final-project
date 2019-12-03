class Move:
    # TODO: give all information to generate next board state (all pieces removed, all pieces added)
    # for simplicity, count moving a piece as removing one piece and adding another somewhere else

    def __init__(self, start, end):
        self._start = start
        self._end = end

class InitialMove(Move):
    def __init__(self, cell):
        self._cell = cell