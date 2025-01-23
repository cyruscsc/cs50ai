"""
Tic Tac Toe Player
"""

import math
import copy

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
    if terminal(board):
        return None

    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board)

    return O if count_X > count_O else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")

    i, j = action

    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O

    # check columns
    for i in range(3):
        col = [board[0][i], board[1][i], board[2][i]]
        if col.count(X) == 3:
            return X
        if col.count(O) == 3:
            return O

    # check diagonals
    diagonals = [[board[0][2], board[1][1], board[2][0]],
                 [board[0][0], board[1][1], board[2][2]]]

    for dia in diagonals:
        if dia.count(X) == 3:
            return X
        if dia.count(O) == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    verdict = winner(board)

    if verdict == X:
        return 1
    if verdict == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        """
        Returns the optimal value and action for the max player.
        """
        if terminal(board):
            return utility(board), None

        value = float('-inf')
        move = None

        for action in actions(board):
            candidate = min_value(result(board, action))[0]

            if candidate > value:
                value = candidate
                move = action

        return value, move

    def min_value(board):
        """
        Returns the optimal value and action for the min player.
        """
        if terminal(board):
            return utility(board), None

        value = float('inf')
        move = None

        for action in actions(board):
            candidate = max_value(result(board, action))[0]

            if candidate < value:
                value = candidate
                move = action

        return value, move

    return max_value(board)[1] if player(board) == X else min_value(board)[1]
