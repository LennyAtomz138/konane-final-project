from board import Board
import copy
import random
import time

static_evaluation_count = 0
number_of_minimax_calls = 0
total_number_of_branches = 0
number_of_cutoffs = 0


class Game:
    def __init__(self, size_of_board, board, player=0, previously_selected_move=((), ())):
        self.size_of_board = size_of_board
        self.konane_board = board
        self.previously_selected_move = previously_selected_move
        self.current_player = player
        self.player_symbol = ('Black Stone', 'White Stone')
        self.finalize_game = 0

    def get_legal_moves(self, current_player):
        """ Returns a list of of legal moves, as pairs of pairs e.g [((8,8),(5,8)),...] """
        legal_moves = []
        for row in range(self.size_of_board):
            for col in range(self.size_of_board):
                if self.konane_board.repr[row][col] == self.player_symbol[current_player]:
                    position = (row, col)
                    move_fn_list = [self.north_move,
                                    self.east_move,
                                    self.south_move,
                                    self.west_move]
                    for move_fn in move_fn_list:
                        move = move_fn(position)
                        if self.is_legal_move(current_player, move):
                            legal_moves.append(move)
                            # now we are going to check for a double jump!
                            start = move[0]
                            cur_end = move[1]
                            # Make a copy of the konane_board, and then make the move on that konane_board.
                            new_board = copy.deepcopy(
                                self.konane_board)
                            new_board.movePiece(start, cur_end)
                            # Try to move again in the same direction.
                            continue_move = move_fn(cur_end)
                            # Make a whole new game state and check if our move is legal on that.
                            new_game_state = Game(self.size_of_board, new_board,
                                                  current_player)
                            while new_game_state.is_legal_move(current_player, continue_move):
                                start_cur = cur_end
                                cur_end = continue_move[1]
                                legal_moves.append((start, cur_end))
                                new_board = copy.deepcopy(new_board)
                                new_board.movePiece(start_cur, cur_end)
                                continue_move = move_fn(cur_end)
                                new_game_state = Game(new_game_state.size_of_board, new_board, current_player)
        return legal_moves

    def is_legal_move(self, current_player, move):
        """ Given a move e.g ((8,8),(5,8)), check if that is legal, return true if it is, false otherwise """
        starting_pos = move[0]
        ending_pos = move[1]
        # Discard any generated moves that fall off of the konane_board.
        if ending_pos[0] not in range(self.size_of_board) or ending_pos[1] not in range(
                self.size_of_board):
            return False
        if self.konane_board.repr[starting_pos[0]][starting_pos[1]] != self.player_symbol[current_player]:
            print("this should never trigger and is redundant")
            return False
        if self.konane_board.repr[ending_pos[0]][ending_pos[1]] != '.':  # Check that landing spot is empty
            return False
        # Check the middle spot is the other piece - this should in theory not matter because the pieces alternate.
        middle_pos = (starting_pos[0] - (starting_pos[0] - ending_pos[0]) / 2,
                      starting_pos[1] - (starting_pos[1] - ending_pos[1]) / 2)
        other_player = 1 - current_player
        if self.konane_board.repr[middle_pos[0]][middle_pos[1]] != self.player_symbol[other_player]:
            return False
        return True

    def generate_next_state(self):
        successors = []
        for move in self.get_legal_moves(self.current_player):
            boardCopy = copy.deepcopy(self.konane_board)
            boardCopy.movePiece(move[0], move[1])
            successors.append(Game(self.size_of_board, boardCopy, 1 - self.current_player, move))
        for s in successors:
            if False:
                print(s.board)
        return successors

    def player_turn(self):
        try:
            legal_moves = self.get_legal_moves(self.current_player)
            print(legal_moves)
            if len(legal_moves) != 0:
                is_valid_input = False
                while not is_valid_input:
                    move_coordinates = (input("Please enter start coordinate: "),
                                        input("Please enter end coordinate: "))  # should be two tuples entered
                    # To convert user input (which is 1 indexed) to 0 indexed (which our konane_board representation is in)
                    actual_move_coordinates = ((move_coordinates[0][0] - 1, move_coordinates[0][1] - 1),
                                               (move_coordinates[1][0] - 1, move_coordinates[1][1] - 1))
                    is_valid_input = actual_move_coordinates in legal_moves
                self.konane_board.movePiece(actual_move_coordinates[0], actual_move_coordinates[1])
                print(self.konane_board)
                self.previously_selected_move = move_coordinates
                self.current_player = 1 - self.current_player
            else:
                self.finalize_game = 1
                print("Player", self.player_symbol[self.current_player], "loses!")
        except KeyboardInterrupt:
            raise
        except:
            print("You messed up, you dingus")
            self.player_turn()

    def computer_turn(self):
        global number_of_minimax_calls
        if len(self.get_legal_moves(self.current_player)) != 0:
            computer_move = minimax_function(self, float("-inf"), float("inf"), 0)
            computer_move = computer_move[1]
            print("FROM BOARD:")
            print(self.konane_board)
            if computer_move is not None:
                self.konane_board.movePiece(computer_move[0], computer_move[1])
                print(self.konane_board)
                print("Made move: ", (
                    (computer_move[0][0] + 1, computer_move[0][1] + 1),
                    (computer_move[1][0] + 1, computer_move[1][1] + 1)))
                self.previously_selected_move = computer_move
                self.current_player = 1 - self.current_player
            else:
                random_move = random.choice(self.get_legal_moves(self.current_player))
                self.konane_board.movePiece(random_move[0], random_move[1])
                print(self.konane_board)
                print("Made move: ", ((random_move[0][0] + 1, random_move[0][1] + 1), (
                    random_move[1][0] + 1, random_move[1][1] + 1)))  # to present the computer's move nicely to player
                self.previously_selected_move = computer_move
                self.current_player = 1 - self.current_player
        else:
            self.finalize_game = 1
            print("Player", self.player_symbol[self.current_player], "loses!")

    @staticmethod
    def north_move(pos):
        return pos, (pos[0] - 2, pos[1])

    @staticmethod
    def east_move(pos):
        return pos, (pos[0], pos[1] + 2)

    @staticmethod
    def south_move(pos):
        return pos, (pos[0] + 2, pos[1])

    @staticmethod
    def west_move(pos):
        return pos, (pos[0], pos[1] - 2)

    def static_evaluation(self):
        my_moves = self.get_legal_moves(0)
        opponent_moves = self.get_legal_moves(1)
        if opponent_moves == 0:
            return float("inf")
        if my_moves == 0:
            return float("-inf")
        return len(my_moves) - len(opponent_moves)


def minimax_function(current_game_state, alpha_term, beta_term, depth_limit):
    # Global is used to modify these variables outside of the scope of this function.
    global number_of_minimax_calls
    global total_number_of_branches
    global static_evaluation_count
    global number_of_cutoffs

    if depth_limit == 4:
        static_evaluation_count += 1
        # The second index of this return statement covers trivial integers.
        return current_game_state.static_evaluation(), None
    # This next block handle's the AI's turn (Max Node):
    elif current_game_state.current_player == 0:
        best_move = None
        number_of_minimax_calls += 1
        for next_game_state in current_game_state.generate_next_state():
            total_number_of_branches += 1
            # AI_move will be relinquished.
            beta_value, AI_move = minimax_function(next_game_state, alpha_term, beta_term, depth_limit + 1)
            if beta_value > alpha_term:
                alpha_term = beta_value
                best_move = next_game_state.last_move_made
            if alpha_term >= beta_term:
                number_of_cutoffs += 1
                return beta_term, best_move
        return alpha_term, best_move
    # This block handle's the Opponent's turn (Min Node):
    else:
        best_move = None
        number_of_minimax_calls += 1
        for next_game_state in current_game_state.generate_next_state():
            total_number_of_branches += 1
            # computer_move is not relevant, we just need to return both for later
            beta_value, computer_move = minimax_function(next_game_state, alpha_term, beta_term, depth_limit + 1)
            if beta_value < beta_term:
                beta_term = beta_value
                best_move = next_game_state.previously_selected_move
            if beta_term <= alpha_term:
                number_of_cutoffs += 1
                return alpha_term, best_move
        return beta_term, best_move


def play_game(game_state):
    print(game_state.board)
    to_remove = input("x remove a piece: ")
    game_state.board.removePiece((to_remove[0] - 1, to_remove[1] - 1))
    print(game_state.board)
    to_remove = input("o remove a piece: ")
    game_state.board.removePiece((to_remove[0] - 1, to_remove[1] - 1))
    while game_state.endgame != 1:
        if game_state.current_player == 0:
            game_state.computer_turn()
        else:
            game_state.computer_turn()


def test_game(game_state):
    game_state.board.removePiece((3, 3))
    print(game_state.board)
    game_state.board.removePiece((3, 2))
    print(game_state.board)
    while game_state.endgame != 1:
        if game_state.current_player == 0:
            game_state.computer_turn()
        else:
            game_state.computer_turn()


if __name__ == '__main__':
    start = time.time()
    test_game(Game(8, Board(8)))
    print("GAME TOOK", time.time() - start, "SECONDS")
    print("NUM STATIC EVALS:", static_evaluation_count)
    print("AVG BRANCHING FACTOR:", total_number_of_branches / (number_of_minimax_calls + 0.0))
    print("NUM CUTOFFS", number_of_cutoffs)
