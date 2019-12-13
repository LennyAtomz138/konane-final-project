from .state import State

class Polynomial:

    limit = 16

    def __init__(self, activeTerms=[], reserveTerms=[]):
        self._active = activeTerms
        self._reserved = reserveTerms

    def evaluate(self, state):
        value = 0
        for t in self._active:
            value += t.coeff() * t.eval(state)
        return value

    def printCoeff(self):
        array = []
        for c in self._active:
            array.append((c.name(), c.coeff()))
        #print(array)
        return array

    def switchOut(self):
        # called at the end of game to increment ltt of lowest coefficient term and switch out if necessary
        minTerm = min(self._active, key=lambda x: x.c)
        minTerm.incLTT()
        if minTerm.ltt >= self.limit:
            minTerm.resetLTT()
            self._active.append(self._reserved.pop(0))
            self._reserved.append(minTerm)
            self._active.remove(minTerm)



"""Following functions are possible evaluators and are based off the Appendix of Samuel's document
Refer to it when defining these functions"""

class PieceAdv():
    def __init__(self, c):
        self._id = "pieceAdv"
        self._c = c

    def eval(self, state):
        b = str(state.board())
        black = 0
        white = 0
        for i in b:
            if i == '■':
                black += 1
            elif i == '□':
                white += 1
        if str(state.color())[-5:] == "white":
            return white - black
        else:
            return black - white

    def coeff(self):
        return self._c

    def name(self):
        return self._id

class Mobility():
    def __init__(self, c):
        self._id = "mobility"
        self._c = c

    def eval(self, state):
        return len(list(state.moves()))

    def coeff(self):
        return self._c

    def name(self):
        return self._id


class DenialOfOccupancy():
    def __init__(self, c):
        self._id = "denialOfOccupancy"
        self._c = c

    def eval(self, state):
        states = list(state.moves())
        total = 0
        for m in states:
            newState = state + m
            total += len(list(newState.moves()))

        if str(state.color())[-5:] == "white":
            return len(states) - total
        else:
            return total - len(states)

    def coeff(self):
        return self._c

    def name(self):
        return self._id

# class ControlOfCenter():
#     def __init__(self):
#         self._id = "controlOfCenter"
#
#     def eval(self, state):
#         pass
#
# NOTE: There are many more terms (26 + 16) found in the manual; would be ideal if we got most of them
