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
    for i in range(len(board)):
        for j in range(len(board[i])):
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
    # return set of i, j

    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions


    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = board.copy()
    #if the current move is an X then place an X on the board
    if player(board) == X:
        board_copy[action[0]][action[1]] = X
        return board_copy
    #if the current move is an O then place an O on the board
    elif player(board) == O:
        board_copy[action[0]][action[1]] = O
        return board_copy
    #else, raise an exception
    else:
        raise Exception("Invalid move")


    #raise NotImplementedError


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
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #if max moves is 9 then game is over
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
    
    #raise NotImplementedError


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

    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    min_value = float("inf")
    max_value = float("-inf")
    best_action = None


    #if player is X then maximize the value
    if player(board) == X:
        while actions(board):
            action = actions(board)
            value = min_value
            if value > max_value:
                max_value = value
                best_action = action
        return best_action
    
    #if player is O then minimize the value
    elif player(board) == O:
        while actions(board):
            action = actions(board)
            value = max_value
            if value < min_value:
                min_value = value
                best_action = action
        return best_action


    raise NotImplementedError
