# Gives an agent the ability to select the next move given a game state
class Player:
    def next_move(self, state):
        raise NotImplementedError

class AIPlayer(Player):
    def next_move(self, state):
        # TODO: minimax (generate states, recursively generate movetree with a/b pruning)
        # a/b pruning is efficient here since move generation is lazy, i.e. done with a generator
        # and not a list. In game tree generation, assume other player is also an AI and call next_move
        # recursively
        for move in state.moves():
            pass
    def _evaluate_state(self, state):
        pass

class NetworkPlayer(Player):
    def next_move(self, state):
        pass

class HumanPlayer(Player):
    def __init__(self, name):
        self._name = name
    
    def next_move(self, state):
        moves = list(state.moves())
        print(f'*** {self._name}\'s move ***')
        print(state)
        print('*** Moves ***')
        print('\n'.join(map(str, enumerate(map(str, moves)))))
        index = int(input('Move: '))
        return moves[index]
    
    def __str__(self):
        return self._name