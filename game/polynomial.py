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
        color = [1,0][state.color()] # If it's black's turn to move, then white chose the move to get to this state
        return 5 # placeholder

    def switchOut(self):
        # called at the end of game to increment ltt of lowest coefficient term and switch out if necessary
        minTerm = min(self._active, key=lambda x: x.c)
        minTerm.incLTT()
        if minTerm.ltt >= self.limit:
            minTerm.resetLTT()
            self._active.append(self._reserved.pop(0))
            self._reserved.append(minTerm)
            self._active.remove(minTerm)


class Term:
    def __init__(self):
        self._id = None
        self._c = 1
        self._ltt = 0

    def id(self):
        return self._id
    
    def c(self):
        return self._c

    def ltt(self):
        return self._ltt

    def incLTT(self):
        self._ltt += 1

    def resetLTT(self):
        self._ltt = 0

    def eval(self, state):
        raise NotImplementedError

    def __eq__(self, other):
        return self._id == other.id


"""Following functions are possible evaluators and are based off the Appendix of Samuel's document
Refer to it when defining these functions"""

""" TODO: implement eval() for each term. Given a state, return the "score" for the board based on the
conditions of the term"""
class PieceAdv(Term):
    def __init__(self):
        self._id = "pieceAdv"

    def eval(self, state):
        pass

class DenialOfOccupancy(Term):
    def __init__(self):
        self._id = "denialOfOccupancy"

    def eval(self, state):
        pass

class Mobility(Term):
    def __init__(self):
        self._id = "mobility"

    def eval(self, state):
        pass

class ControlOfCenter(Term):
    def __init__(self):
        self._id = "controlOfCenter"

    def eval(self, state):
        pass

class PieceAdvancement(Term):
    def __init__(self):
        self._id = "pieceAdvancement"

    def eval(self, state):
        pass

# NOTE: There are many more terms (26 + 16) found in the manual; would be ideal if we got most of them
