class Player:
    def __init__(self, color):
        self._color = color

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

class NetworkPlayer(Player):
    def next_move(self, state):
        pass