"""
Tic Tac Toe Player
"""

from ctypes import util
import math
from copy import deepcopy

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
    if sum([place != EMPTY for place in list(board)]) % 2 == 0:
        player = X
    else:
        player = O

    return player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(len(board)):
        for cell in range(len(board)):
            if board[row][cell] == EMPTY:
                actions.add((row, cell))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise "Invalid Action"

    copy_board = deepcopy(board)
    copy_board[action[0]][action[1]] = player(board)

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows
    all_rows = [set(row) for row in board]
    for row in all_rows:
        if len(row) <= 1:
            winner = row.pop()
            if winner != EMPTY:
                return winner

    # Check columns
    all_columns = [set() for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board)):
            all_columns[j].add(board[i][j])

    for column in all_columns:
        if len(column) <= 1:
            winner = column.pop()
            if winner != EMPTY:
                return winner

    # Check diagonals
    main_diagonal = set()
    main_diagonal.add(board[0][0])
    main_diagonal.add(board[1][1])
    main_diagonal.add(board[2][2])
    off_diagonal = set()
    off_diagonal.add(board[0][2])
    off_diagonal.add(board[1][1])
    off_diagonal.add(board[2][0])

    for diagonal in [main_diagonal, off_diagonal]:
        if len(diagonal) <= 1:
            winner = diagonal.pop()
            if winner != EMPTY:
                return winner

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    list_board = []
    for row in board:
        list_board = list_board + row

    if list_board.count(EMPTY) == 0:
        return True
    elif winner(board) != None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)
    if player == X:
        return 1
    elif player == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    local_player = player(board)
    optimal_action = None

    if local_player == X:
        v = -math.inf
        for action in actions(board):
            maximal = max_value(result(board, action))
            if maximal > v:
                optimal_action = action
                v = maximal
    elif local_player == O:
        v = math.inf
        for action in actions(board):
            minimal = min_value(result(board, action))
            if minimal < v:
                optimal_action = action
                v = minimal

    return optimal_action
