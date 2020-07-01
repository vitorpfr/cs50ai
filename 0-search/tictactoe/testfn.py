from tictactoe import player, actions, result, player_is_winner, terminal, utility, minimax

X = "X"
O = "O"
EMPTY = None

board = [[O, EMPTY, X],
         [X, EMPTY, EMPTY],
         [X, O, O]]

# Testing player function
# print("testing")
# board_result = player(board)
# print(board_result)
# Should return X or O

# Testing actions function
# print("testing")
# board_actions = actions(board)
# print(board_actions)
# Should return all fields where board is EMPTY

# Testing result function
# print("testing")
# board_result = result(board, (1, 1))
# print(board_result)
# Should return the board after the action

# Testing player_is_winner function
# print("testing")
# player_is_winner_result = player_is_winner(board, X)
# print(player_is_winner_result)

# Testing terminal function
# print("testing")
# terminal_result = terminal(board)
# print(terminal_result)

# Testing utility function
# print("testing")
# utility_result = utility(board)
# print(utility_result)

# Testing minimax function
print("testing")
minimax_result = minimax(board)
print("minimax result: ")
print(minimax_result)
