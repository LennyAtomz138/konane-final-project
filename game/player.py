cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']
# Gives an agent the ability to select the next move given a game state
class Player:
    def next_move(self, state):
        raise NotImplementedError

def encode_for_server(arg):
    #recieves 'Remove (int, char)' or '(int, char) -> (int, char)'
    if '->' in arg: # not first move
        res = arg.split('->')
        print("Moving encoding:")
        print(res)
        return "["+str(int(res[0][1])-1)+":"+str(cols.index(res[0][4]))+"]"+":"+"["+str(int(res[1][2])-1)+":"+str(cols.index(res[1][5]))+"]"
    else:
        res = arg[7:]
        print("Removing encoding:")
        print(res)
        return "["+str(int(res[1])-1)+":"+str(cols.index(res[4]))+"]"

def decode_from_server(arg):
    if ']:[' in arg: #not first move
        #[2:0]:[0:0]
        print("Moving decoding:")
        print(arg)
        res = arg[4:]
        return "("+str(int(res[1])+1)+", "+cols[int(res[3])]+") -> (" +str(int(res[7])+1)+", "+cols[int(res[9])]+")"
    else:
        print("Removing decoding:")
        print(arg)
        #Removed:[0:0]
        res = arg[1][8:]
        return "("+str(int(res[1])+1)+", "+cols[int(res[3])]+")"

# Gets next move via Minimax and knowledge base
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
        if (self.tn is not None):
            options = []
            for i in moves:
                options.append(str(i))
            self.tn.write(encode_for_server(options[index]).encode('ascii')+b"\r\n")
        #updates our board
        return moves[index]

    def _evaluate_state(self, state):
        pass

# Gets next move from network
class NetworkPlayer(Player):
    def __init__(self, connection, start = None):
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
        if (self.flag and self.first is not None):
            #get first remove from the network and play that
            res = self.first.split('\n')
            print(res)
            op_move = res
            self.flag = False
        else:
            while True:
                stri = self.tn.read_some()
                serv = str(stri, "utf-8")
                print(serv)
                if "Error:" in serv:
                    return None
                if "win" in serv:
                    return None
                #if "Remove" in op_move and self.flag:

                if "Move" in serv:
                    print(serv)
                    op_move = serv#.split('\n')
                    break

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

# Gets next move from user input
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
