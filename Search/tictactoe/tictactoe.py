"""
Tic Tac Toe Player
"""

# https://submit.cs50.io/check50/ca39412a8b1cedd9162d701288ce87ad2b154dd2

import copy
import math

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
    # Count how many X and Os on the board
    # if len(X) <= len(O) then it's X's turn because X goes first
    # return X
    # else it's O's turn
    # return O

    x_count = 0
    o_count = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1

    if x_count <= o_count:
        # print(f"X's turn...")
        return X
    elif x_count > o_count:
        # print(f"O's turn...")
        return O
    else:
        raise Exception("Invalid player")

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # if board[i][j] == EMPTY then it's a possible action
    # return set of i, j

    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    # print(f"possible actions: {possible_actions}")
    return possible_actions

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    current_player = player(board)

    if action is None:
        raise ValueError("Action cannot be None")

    if board_copy[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action: Cell is not empty")

    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise ValueError("Action coordinates out of bounds")


    board_copy[action[0]][action[1]] = current_player
    return board_copy

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    case1 = board[0][0] == board[0][1] == board[0][2] != None
    case2 = board[1][0] == board[1][1] == board[1][2] != None
    case3 = board[2][0] == board[2][1] == board[2][2] != None
    case4 = board[0][0] == board[1][0] == board[2][0] != None
    case5 = board[0][1] == board[1][1] == board[2][1] != None
    case6 = board[0][2] == board[1][2] == board[2][2] != None
    case7 = board[0][0] == board[1][1] == board[2][2] != None
    case8 = board[0][2] == board[1][1] == board[2][0] != None

    if case1 or case2 or case3 or case4 or case5 or case6 or case7 or case8:
        if player(board) == X:
            return O
        else:
            return X
    return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if max moves is 9 then game is over
    x_count = 0
    o_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1
    if x_count + o_count == 9:
        return True

    elif winner(board) != None:
        return True
    else:
        return False

    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Max Value function
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    # Min Value function
    def min_value(board):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    best_action = None

    if terminal(board):
        return None

    current_player = player(board)

    if current_player == O:
        min_v = math.inf
        for action in actions(board):
            v = max_value(result(board, action))
            if v < min_v:
                min_v = v
                best_action = action
    else:
        max_v = -math.inf
        for action in actions(board):
            v = min_value(result(board, action))
            if v > max_v:
                max_v = v
                best_action = action

    return best_action

    # raise NotImplementedError
