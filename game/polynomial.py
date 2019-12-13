from .state import State

class Polynomial:

    limit = 16

    def __init__(self, activeTerms=[], reserveTerms=[]):
        self._active = activeTerms
        self._reserved = reserveTerms

    """TODO: Evaluate a state's score using the polynomial. This means adding up all term evaluations from
        the self._active array and returning this value. This can only be done AFTER the terms have been
        defined, so do that first! """
    def evaluate(self, state):
        #color = [1,0][state.color()] # If it's black's turn to move, then white chose the move to get to this state
        value = 0
        b = str(state.board())
        black = 0
        white = 0
        dom = 0
        for i in b:
            if i == '■':
                black += 1
            elif i == '□':
                white += 1
        if black > white:
            dom = ("black", black)
        else:
            dom = ("white", white)
        for t in self._active:
            value += t.coeff() * t.eval(state, dom)
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


# class Term:
#     def __init__(self):
#         self._id = None
#         self.c = 1
#         self._ltt = 0
#
#     def id(self):
#         return self._id
#
#     # def c(self):
#     #     return self._c
#
#     def ltt(self):
#         return self._ltt
#
#     def incLTT(self):
#         self._ltt += 1
#
#     def resetLTT(self):
#         self._ltt = 0
#
#     def eval(self, state, color):
#         raise NotImplementedError
#
#     def __eq__(self, other):
#         return self._id == other.id


"""Following functions are possible evaluators and are based off the Appendix of Samuel's document
Refer to it when defining these functions"""

""" TODO: implement eval() for each term. Given a state, return the "score" for the board based on the
conditions of the term"""
class PieceAdv():
    def __init__(self, c):
        self._id = "pieceAdv"
        self._c = c

    def eval(self, state, dom):
        sign = 1
        if str(state.color())[-5:] == "white" and dom[0] == "white":
            sign = -1
        elif  str(state.color())[-5:] == "black" and dom[0] == "black":
            sign = -1
        rem = state.board().n_removed()
        value = 1
        if rem < 145:
            value = rem
        else:
            value = state.board().n_occupied() - 37
        return sign * rem

    def coeff(self):
        return self._c

    def name(self):
        return self._id

class Mobility():
    def __init__(self, c):
        self._id = "mobility"
        self._c = c

    def eval(self, state, dom):
        sign = 1
        if str(state.color())[-5:] == "white" and dom[0] == "white":
            sign = -1
        elif  str(state.color())[-5:] == "black" and dom[0] == "black":
            sign = -1
        rem = state.board().n_removed()
        value = 1
        if rem > 250:
            value = len(list(state.moves()))
        return sign * value

    def coeff(self):
        return self._c

    def name(self):
        return self._id

# class DenialOfOccupancy(Term):
#     def __init__(self):
#         self._id = "denialOfOccupancy"
#
#     def eval(self, state):
#         pass
#
# class Mobility(Term):
#     def __init__(self):
#         self._id = "mobility"
#
#     def eval(self, state):
#         pass
#
# class ControlOfCenter(Term):
#     def __init__(self):
#         self._id = "controlOfCenter"
#
#     def eval(self, state):
#         pass
#
# class PieceAdvancement(Term):
#     def __init__(self):
#         self._id = "pieceAdvancement"
#
#     def eval(self, state):
#         pass

# NOTE: There are many more terms (26 + 16) found in the manual; would be ideal if we got most of them
