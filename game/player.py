import pickle
import math
from .polynomial import *
import json
import random

cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']


# Gives an agent the ability to select the next move given a game state
class Player:
    def next_move(self, state):
        raise NotImplementedError


def encode_for_server(arg):
    # Receives 'Remove (int, char)' or '(int, char) -> (int, char)'
    if '->' in arg:  # not first move
        res = arg.split('->')
        print("Moving encoding:")
        print(res)
        # ['(3, a) ', ' (1, a)']
        p1 = tuple(map(str, res[0].replace(' ', '')[1:-1].split(',')))
        p2 = tuple(map(str, res[1].replace(' ', '')[1:-1].split(',')))
        return "[" + str(int(p1[0]) - 1) + ":" + str(cols.index(p1[1])) + "]" + ":" + "[" + str(
            int(p2[0]) - 1) + ":" + str(cols.index(p2[1])) + "]"
    else:
        res = arg[7:]
        print("Removing encoding:")
        print(res)
        # (1, a)
        p1 = tuple(map(str, res.replace(' ', '')[1:-1].split(',')))
        return "[" + str(int(p1[0]) - 1) + ":" + str(cols.index(p1[1])) + "]"


def decode_from_server(arg):
    if ']:[' in arg:  # not first move
        res = arg[4:]
        print("Moving decoding:")
        print(res)
        # [2:0]:[0:0]
        res = res.replace("]:[", "],[").split(",")
        p1 = json.loads(res[0].replace(":", ","))
        p2 = json.loads(res[1].replace(":", ","))

        return "(" + str(int(p1[0]) + 1) + ", " + cols[int(p1[1])] + ") -> (" + str(int(p2[0]) + 1) + ", " + cols[
            int(p2[1])] + ")"
    else:
        res = arg[8:]
        print("Removing decoding:")
        print(res)
        # [0:0]
        p1 = json.loads(res.replace(":", ","))
        return "(" + str(int(p1[0]) + 1) + ", " + cols[int(p1[1])] + ")"


# Gets next move via Minimax and knowledge base
# Learning AIs keep track of path (state, score) for reward later
class AIPlayer(Player):
    def __init__(self, connection=None, learn=True):
        self.tn = connection
        self._learn = learn
        if learn:
            self._name = "Learner"
            prev = pickle.load(open('Memory/polynomial.data', 'rb')).printCoeff()
            self._polynomial = Polynomial([PieceAdv(random.uniform(prev[0][1] - .25, prev[0][1] + .25)),
                                           Mobility(random.uniform(prev[1][1] - .25, prev[1][1] + .25)),
                                           DenialOfOccupancy(random.uniform(prev[2][1] - .25, prev[2][1] + .25))], [])
            self._path = []
        else:
            self._name = "Motley Crew"
            self._polynomial = pickle.load(open('Memory/polynomial.data', 'rb'))

    # Returns the best-worst-case (next move, score)
    def _minimax(self, curState, depth=2, alpha=-math.inf, beta=math.inf, maxPlayer=True):
        if depth == 0 or curState.is_loss():
            return None, self._polynomial.evaluate(curState)
        elif maxPlayer:
            maxEval = -math.inf
            bestMove = None
            for move in list(curState.moves()):
                curr_eval = self._minimax(curState + move, depth - 1, alpha, beta, False)[1]
                if maxEval < curr_eval:
                    maxEval = curr_eval
                    bestMove = move
                alpha = max(alpha, curr_eval)
                if beta <= alpha:
                    break
            return bestMove, maxEval
        else:
            minEval = math.inf
            bestMove = None
            for move in list(curState.moves()):
                curr_eval = self._minimax(curState + move, depth - 1, alpha, beta, True)[1]
                if minEval > curr_eval:
                    minEval = curr_eval
                    bestMove = move
                beta = min(beta, curr_eval)
                if beta <= alpha:
                    break
            return bestMove, minEval

    def next_move(self, state):
        print(f'*** {self._name}\'s move ***')
        print(state)

        # if self._learn:
        #     bestMove = self._minimax(curState=state)[0]
        #     print("Best move:")
        #     print(bestMove)
        # else:
        #     moves = list(state.moves())
        #     bestMove = moves[0]
        #     print("Best move:")
        #     print(bestMove)
        bestMove = self._minimax(curState=state)[0]
        print("Best move:")
        print(bestMove)

        # If learning, save each new position and its static evaluation to self._path
        # if self._learn:
        #     if state.board().n_removed() <= 1:
        #         self._path.append((state, self._polynomial.evaluate(state)))
        #     newState = state + bestMove
        #     self._path.append((newState, self._polynomial.evaluate(newState)))
        #     #print(self._path)

        if self.tn is not None:
            self.tn.write(encode_for_server(str(bestMove)).encode('ascii') + b"\r\n")
        return bestMove

    def getPath(self):
        return self._path

    def getPoly(self):
        return self._polynomial

    def __str__(self):
        return self._name


# Gets next move from network
class NetworkPlayer(Player):
    def __init__(self, connection, start=None):
        self.tn = connection
        self._name = "Server Opponent"
        self.first = start
        self.flag = True

    def next_move(self, state):
        moves = list(state.moves())
        options = []
        index = []
        choice = ''
        op_move = ''
        print(f'*** {self._name}\'s move ***')
        print(state)

        if self.flag and self.first is not None:
            #  Get first remove from the network and play that
            res = self.first.split('\n')
            print(res)
            op_move = res[1]
            self.flag = False
        else:
            buffer = []
            while True:
                stri = self.tn.read_some()
                serv = str(stri, "utf-8")
                print(serv)
                buffer.append(serv)
                if "Error:" in serv:
                    return None
                if "win" in serv:
                    return None
                if "?Move" in serv:
                    op_move = buffer[-2]  # .split('\n')
                    break

        #  Convert server choice to our game's move format
        choice = decode_from_server(op_move)

        for i in moves:
            options.append(str(i))
        #  Find the choice's index from list of moves
        for s in options:
            if choice in s:
                index = options.index(s)
        if index == []:
            print(choice)
            print('\n'.join(map(str, enumerate(map(str, moves)))))
            print("Could not find Opponent's move.....")
        return moves[index]

    def __str__(self):
        return self._name


# Gets next move from user input
class HumanPlayer(Player):
    def __init__(self, name, connection=None):
        self._name = name
        self.tn = connection

    def next_move(self, state):
        moves = list(state.moves())
        print(f'*** {self._name}\'s move ***')
        print(state)
        print('*** Moves ***')
        print('\n'.join(map(str, enumerate(map(str, moves)))))
        index = int(input('Move: '))
        if self.tn is not None:
            self.tn.write(encode_for_server(str(moves[index])).encode('ascii') + b"\r\n")
        return moves[index]

    def __str__(self):
        return self._name
