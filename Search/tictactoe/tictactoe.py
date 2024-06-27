"""
Tic Tac Toe Player
"""

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
    # if len(X) <= len(O) then it's X's turn
    # return X
    # else it's O's turn
    # return O
    
    x_count = 0
    o_count = 0
    for i in range(board):
        for j in range(board[i]):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1
    if x_count <= o_count:
        print(f"X's turn...")
        return X
    else:
        print(f"O's turn...")
        return O


    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # if board[i][j] == EMPTY then it's a possible action
    # return i, j

    possible_actions = set()

    for i in range(board):
        for j in range(board[i]):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions


    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #if max moves is 9 then game is over
    x_count = 0
    o_count = 0
    for i in range(board):
        for j in range(board[i]):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1
    if x_count + o_count == 9:
        return True
    
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
