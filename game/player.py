cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']
# Gives an agent the ability to select the next move given a game state
class Player:
    def next_move(self, state):
        raise NotImplementedError


def encode_for_server(arg):
    #recieves 'Remove (int, char)' or '(int, char) -> (int, char)'
    if '->' in arg: # not first move
        res = arg.split('->')
        return "["+str(int(res[0][1])-1)+":"+cols.index(res[0][4])+"]"+":"+"["+str(int(res[1][1])-1)+":"+cols.index(res[1][4])+"]"
    else:
        res = arg[7:]
        print(res)
        return "["+str(int(res[1])-1)+":"+cols.index(res[4])+"]"

def decode_from_server(arg):
    if ']:[' in arg: #not first move
        return #() -> () format
    else:
        return # ()

class AIPlayer(Player):
    def __init__(self, connection = None):
        self.tn = connection
        self._name = "Motley Crew"

    def next_move(self, state):
        # TODO: minimax (generate states, recursively generate movetree with a/b pruning)
        # a/b pruning is efficient here since move generation is lazy, i.e. done with a generator
        # and not a list. In game tree generation, assume other player is also an AI and call next_move
        # recursively
        # for move in state.moves():
        #     pass
        moves = list(state.moves())
        print(f'*** {self._name}\'s move ***')
        print(state)

        ##Make this part evaluate moves and return the index of the move it chose to play
        print('*** Moves ***')
        print('\n'.join(map(str, enumerate(map(str, moves)))))
        index = int(input('Move: '))
        ################################################

        #Uses index to find the chosen move, converts it to server format, and sends it
        if (self.connection is not None):
            options = []
            for i in moves:
                options.append(str(i))
            self.tn.write(encode_for_server(options[index]).encode('ascii')+b"\r\n")
        #updates our board
        return moves[index]

    def _evaluate_state(self, state):
        pass

class NetworkPlayer(Player):
    def __init__(self, connection, start = ''):
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
        #Checks if we are first (0) or second (1) to move
        if (self.flag):
            #get first remove from the network and play that
            print(self.first)
            res = self.first.split('\n')
            op_move = res[1]
            self.flag = False
        else:
            op_move = self.tn.read_some()
            print(str(op_move, "utf-8"))

        ####Convert server choice to our game's move format
        choice = decode_from_server(op_move)

        for i in moves:
            options.append(str(i))
        #Find the choice's index from list of moves
        for s in options:
            if choice in s:
                index = options.index(s)
        if (index == []):
            print("Could not find Opponent's move.....")
        return moves[index]

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
