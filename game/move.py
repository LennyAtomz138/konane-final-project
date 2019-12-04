class Move:
    def __init__(self, start, end):
        self._start = start
        self._end = end
        
    def added(self):
        return [self._end]
    
    def removed(self):
        d = self._end - self._start
        dist = abs(sum(d))
        v = (d[0]/dist, d[1]/dist)
        result = [self._start]
        ptr = self._start + v
        while len(result) < dist / 2:
            result.append(ptr)
            ptr = ptr + v + v
        return result

    def __str__(self):
        return f'{self._start} -> {self._end}'


class InitialMove(Move):
    def __init__(self, cell):
        self._cell = cell
    
    def added(self):
        return []

    def removed(self):
        return [self._cell]

    def __str__(self):
        return f'Remove {self._cell}'