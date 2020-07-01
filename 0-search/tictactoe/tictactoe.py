"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Creates a flat board
    flat_board = [item for sublist in board for item in sublist]

    # Check past moves: if X has same number of moves as O, it's X time
    if flat_board.count(X) == flat_board.count(O):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Create empty set to store actions
    empty_spaces = set()

    # Iterate through board and add empty spaces to set, returning it when done
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == EMPTY:
                empty_spaces.add((i, j))
    return empty_spaces


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Makes a copy of the board (to avoid changing the previous one)
    board_after_action = deepcopy(board)

    # Check if input is in tuple format
    try:
        i, j = action
    except:
        raise Exception("action input is not in the tuple format")

    # Check if coordinates are int, if so, change the board with the action
    if isinstance(i, int) and isinstance(j, int):
        board_after_action[i][j] = player(board)
    else:
        raise Exception("move indexes are not integers")

    return board_after_action


def player_is_winner(board, player):
    """
    Returns True if player is the winner in the given board, or False otherwise.
    """
    # Define winning criteria for each possible win: horizontal, vertical or diagonal
    horizontal_win = any(all(x == player for x in row) for row in board)
    vertical_win = any(all(x == player for x in row) for row in [list(i) for i in zip(*board)])
    diagonal_win = all(x == player for x in np.diag(board)) or all(x == player for x in np.flipud(board).diagonal(0)[::-1])

    # Return true if any of those are true (it means this player won)
    return (horizontal_win or vertical_win or diagonal_win)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if each player on, return None otherwise
    if player_is_winner(board, X):
        return X
    if player_is_winner(board, O):
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Creates a flat board
    flat_board = [item for sublist in board for item in sublist]

    # Check two terminal conditions: either someone won or the board is filled
    game_has_a_winner = (not (winner(board) == None))
    board_completely_filled = (not (None in flat_board))

    return (game_has_a_winner or board_completely_filled)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def max_value(board, alpha, beta):
    """
    Returns maximum value of state as output
    """
    # If board received is terminal, return its utility
    if terminal(board):
        return utility(board)

    # Iterate through possible actions on board and return the maximum value of the possible opponent actions, which is optimizing for min
    # If it's impossible to get a better value, break for loop
    value = float('-inf')
    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value


def min_value(board, alpha, beta):
    """
    Returns minimum value of state as output
    """
    # If board received is terminal, return its utility
    if terminal(board):
        return utility(board)

    # Iterate through possible actions on board and return the minimum value of the possible opponent actions, which is optimizing for max
    # If it's impossible to get a better value, break for loop
    value = float('inf')
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If board is terminal, there's no possible action
    if terminal(board):
        return None

    # Create empty dict to store possible actions and their utility value
    actions_to_value = {}

    # Verify which player is playing, iterate through possible actions and give a value to each one of them
    # Return the action with max value for player X, or action with min value for player O
    if player(board) == X:
        for action in actions(board):
            actions_to_value[action] = min_value(result(board, action), float('-inf'), float('inf'))
        return max(actions_to_value, key=actions_to_value.get)

    if player(board) == O:
        for action in actions(board):
            actions_to_value[action] = max_value(result(board, action), float('-inf'), float('inf'))
        return min(actions_to_value, key=actions_to_value.get)