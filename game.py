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

    def find_legal_moves(self, current_player):
        """ Returns a list of of legal moves, as tuple of tuples e.g [((5,5),(4,6)),...]. """
        legal_moves_list = []
        for row in range(self.size_of_board):
            for column in range(self.size_of_board):

                # Note that .repr is used to here to limit the size of the search scope.
                if self.konane_board.repr[row][column] == self.player_symbol[current_player]:
                    current_position = (row, column)
                    list_of_possible_moves = \
                        [self.upward_move,
                         self.rightward_move,
                         self.downward_move,
                         self.leftward_move]
                    for possible_move in list_of_possible_moves:

                        current_move = possible_move(current_position)
                        if self.determine_move_legality(current_player, current_move):
                            legal_moves_list.append(current_move)
                            # Next, scan for the possibility of a double-jump.
                            begin_scan = current_move[0]
                            end_of_current_scan = current_move[1]
                            # Utilize a copy of the Konane board for a test run of the scanned move.
                            # Note that copy.deepcopy() is used here in order to keep a table of objects that have
                            # already been copied during a given copying pass.
                            copied_board = copy.deepcopy(self.konane_board)
                            copied_board.move_konane_stone(begin_scan, end_of_current_scan)
                            # Try to current_move again in the same direction.
                            continue_move_scan = possible_move(end_of_current_scan)

                            # Instantiate an experimental game state and ensure that current move is still legal there.
                            experimental_game_state = Game(self.size_of_board, copied_board, current_player)
                            while experimental_game_state.determine_move_legality(current_player, continue_move_scan):
                                current_start_position = end_of_current_scan
                                end_of_current_scan = continue_move_scan[1]
                                legal_moves_list.append((begin_scan, end_of_current_scan))
                                copied_board = copy.deepcopy(copied_board)
                                copied_board.move_konane_stone(current_start_position, end_of_current_scan)
                                continue_move_scan = possible_move(end_of_current_scan)
                                experimental_game_state = Game(experimental_game_state.size_of_board,
                                                               copied_board, current_player)
        return legal_moves_list

    def determine_move_legality(self, current_player, current_move_pair):
        """ Given a current_move_pair e.g ((5,5),(4,6)), determine its legality: return True or False respectively. """
        initial_position = current_move_pair[0]
        final_position = current_move_pair[1]

        # Remove potential moves that would place the stone out of the bounds of the board:
        if final_position[0] not in range(self.size_of_board) or final_position[1] not in range(self.size_of_board):
            return False

        # Ensure that the landing point is empty:
        if self.konane_board.repr[final_position[0]][final_position[1]] != '.':
            return False

        # Ensure that the player is the legal player:
        if self.konane_board.repr[initial_position[0]][initial_position[1]] != self.player_symbol[current_player]:
            print("Somehow, this player is not the legal player for this move.")
            return False

        # Ensure that the midpoint between the initial and final positions is the opponent's stone:
        midpoint_position = (initial_position[0] - (initial_position[0] - final_position[0]) / 2,
                             initial_position[1] - (initial_position[1] - final_position[1]) / 2)
        opponent = 1 - current_player
        if self.konane_board.repr[midpoint_position[0]][midpoint_position[1]] != self.player_symbol[opponent]:
            return False

        return True

    def generate_next_state(self):
        list_of_next_states = []

        for legal_move in self.find_legal_moves(self.current_player):
            board_deep_copy = copy.deepcopy(self.konane_board)
            board_deep_copy.move_konane_stone(legal_move[0], legal_move[1])
            list_of_next_states.append(Game(self.size_of_board, board_deep_copy, 1 - self.current_player, legal_move))

        for valid_state in list_of_next_states:
            if False:
                print(valid_state.board)

        return list_of_next_states

    def player_turn(self):
        try:
            legal_moves = self.find_legal_moves(self.current_player)
            print(legal_moves)
            if len(legal_moves) != 0:
                is_current_input_valid = False
                while not is_current_input_valid:
                    # Game will prompt user for two tuples as input:
                    movement_coordinates = (input("Input starting coordinates: "),
                                            input("Input ending coordinate: "))
                    # Revert coordinates to 0-indexed representation in order to align with Konane board configuration.
                    zero_indexed_movement_coordinates = (
                        (movement_coordinates[0][0] - 1, movement_coordinates[0][1] - 1),
                        (movement_coordinates[1][0] - 1, movement_coordinates[1][1] - 1))
                    is_current_input_valid = zero_indexed_movement_coordinates in legal_moves
                self.konane_board.move_konane_stone(zero_indexed_movement_coordinates[0], zero_indexed_movement_coordinates[1])
                print(self.konane_board)
                self.previously_selected_move = movement_coordinates
                self.current_player = 1 - self.current_player
            else:
                self.finalize_game = 1
                print("Player", self.player_symbol[self.current_player], "loses!")
        except KeyboardInterrupt:
            raise
        except:
            print("You messed up, you dingus")
            self.player_turn()

    def opponent_turn(self):
        global number_of_minimax_calls
        if len(self.find_legal_moves(self.current_player)) != 0:
            computer_move = minimax_function(self, float("-inf"), float("inf"), 0)
            computer_move = computer_move[1]
            print("FROM BOARD:")
            print(self.konane_board)
            if computer_move is not None:
                self.konane_board.move_konane_stone(computer_move[0], computer_move[1])
                print(self.konane_board)
                print("Made move: ", (
                    (computer_move[0][0] + 1, computer_move[0][1] + 1),
                    (computer_move[1][0] + 1, computer_move[1][1] + 1)))
                self.previously_selected_move = computer_move
                self.current_player = 1 - self.current_player
            else:
                random_move = random.choice(self.find_legal_moves(self.current_player))
                self.konane_board.move_konane_stone(random_move[0], random_move[1])
                print(self.konane_board)
                print("Made move: ", ((random_move[0][0] + 1, random_move[0][1] + 1), (
                    random_move[1][0] + 1, random_move[1][1] + 1)))  # to present the computer's move nicely to player
                self.previously_selected_move = computer_move
                self.current_player = 1 - self.current_player
        else:
            self.finalize_game = 1
            print("Player", self.player_symbol[self.current_player], "loses!")

    @staticmethod
    def upward_move(pos):
        return pos, (pos[0] - 2, pos[1])

    @staticmethod
    def rightward_move(pos):
        return pos, (pos[0], pos[1] + 2)

    @staticmethod
    def downward_move(pos):
        return pos, (pos[0] + 2, pos[1])

    @staticmethod
    def leftward_move(pos):
        return pos, (pos[0], pos[1] - 2)

    def static_evaluation(self):
        my_moves = self.find_legal_moves(0)
        opponent_moves = self.find_legal_moves(1)
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
            game_state.opponent_turn()
        else:
            game_state.opponent_turn()


def test_game(game_state):
    game_state.board.removePiece((3, 3))
    print(game_state.board)
    game_state.board.removePiece((3, 2))
    print(game_state.board)
    while game_state.endgame != 1:
        if game_state.current_player == 0:
            game_state.opponent_turn()
        else:
            game_state.opponent_turn()


if __name__ == '__main__':
    start = time.time()
    test_game(Game(8, Board(8)))
    print("GAME TOOK", time.time() - start, "SECONDS")
    print("NUM STATIC EVALS:", static_evaluation_count)
    print("AVG BRANCHING FACTOR:", total_number_of_branches / (number_of_minimax_calls + 0.0))
    print("NUM CUTOFFS", number_of_cutoffs)
