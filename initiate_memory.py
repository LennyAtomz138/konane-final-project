import pickle
from game.polynomial import *

""" Run createNewMemory in order to refresh polynomial.data with a new polynomial object, which will reset all
coefficients and terms with the default

Do NOT do this unless we are starting over with learning!"""

# TODO: Finish defining terms, then run this function to generate a starting memory so we can start training
def createNewMemory():
    activeTerms = [PieceAdv(1), Mobility(1), DenialOfOccupancy(1)]# ControlOfCenter()]
    reservedTerms = [] # for overflowing terms

    polynomial = Polynomial(activeTerms, reservedTerms)
    open('Memory/polynomial.data', 'w').close() # erase contents
    pickle.dump(polynomial, open('Memory/polynomial.data', 'wb'))

if __name__ == '__main__':
    createNewMemory()
