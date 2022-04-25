"""
Tic Tac Toe Player
This program uses a minimax algorithm to find the maximum scoring move while minimizing the
opponent's score.  Currently chokes on first move, as it analyzes every move.  Could be improved
using alpha beta pruning or depth limiting.
"""
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
    x_count=0
    o_count=0
    for i in range(len(board)):
        for j in board[i]:
            if 'X' == j:
                x_count+=1
            if 'O' == j:
                o_count+=1
    #print(x_count,o_count)
    if x_count > o_count:
        return 'O'
    else:
        return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    my_set = set()
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                my_set.add((row,column))
    #print(my_set)
    return my_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("action not valid")
    i = action[0]
    j = action[1]
    user = player(board)
    board_clone = copy.deepcopy(board)
    board_clone[i][j] = user
    return board_clone

# def undo(board, action):
#     """
#     Unneeded function when result is implemented properly with a deepcopy of the board.
#     """
#     i = action[0]
#     j = action[1]
#     user = player(board)
#     board[i][j] = EMPTY
#     return board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i] == ['X','X','X']:
            return 'X'
    if board[0][0] == board[1][0] == board[2][0] == 'X' or board[0][1] == board[1][1] == board[2][1] =='X' or board[0][2] == board[1][2] == board[2][2] == 'X':
        return 'X'
    if board[0][0] == board[1][1] == board[2][2] == 'X' or board[2][0] == board[1][1] == board[0][2] == 'X':
        return 'X'

    for i in range(len(board)):
        if board[i] == ['O','O','O']:
            return 'O'
    if board[0][0] == board[1][0] == board[2][0] =='O' or board[0][1] == board[1][1] == board[2][1] =='O' or board[0][2] == board[1][2] == board[2][2] =='O':
        return 'O'
    if board[0][0] == board[1][1] == board[2][2] =='O' or board[2][0] == board[1][1] == board[0][2] =='O':
        return 'O'

    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for i in range(len(board)):
        if board[i] == ['X','X','X'] or board[i] == ['O','O','O']:
            #print('game over horizontal')
            return True
    if board[0][0] == board[1][0] == board[2][0] != None or board[0][1] == board[1][1] == board[2][1] != None or board[0][2] == board[1][2] == board[2][2] != None:
        #print('game over vertical')
        return True
    if board[0][0] == board[1][1] == board[2][2] != None or board[2][0] == board[1][1] == board[0][2] != None:
        #print('game over diagonal')
        return True
    if not actions(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    my_set = actions(board)
    if player(board) == 'O':
        v=math.inf
        v_prev=v
        for action in my_set:
            v=maxi(result(board,action))
            print(f'action {action} score {v}')
            if v<v_prev:
                best_action=action
                v_prev=v
            # if v == -1:
            #     return best_action #skip looking once a winning action is revealed.
            #undo(board,action)
        print(f'best action {best_action} score {v_prev}')
        return best_action
    else:
        v=-math.inf
        v_prev=v
        for action in my_set:
            v=mini(result(board,action))
            print(f'action {action} score {v}')
            if v>v_prev:
                best_action=action
                v_prev=v
            #undo(board,action)
            # if v == 1:
            #     return best_action #skip looking once a winning action is revealed.
        print(f'best action {best_action} score {v_prev}')
        return best_action

def mini(board):
    """
    Returns minimum number of points
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    v_prev=v
    my_set = actions(board)
    for action in my_set:
        #print(f'this action min {action}')
        v = maxi(result(board,action))
        if v<v_prev:
            v_prev=v
        # if v == -1:
        #     return v #stop looking once win
        #undo(board,action)
    print(f'v_prev mini = {v_prev}')
    return v_prev

def maxi(board):
    """
    Returns maximum number of points
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    v_prev = v
    my_set = actions(board)
    for action in my_set:
        #print(f'this action {action}')
        v = mini(result(board,action))
        if v>v_prev:
            v_prev=v
        # if v == 1:
        #     return v #stop looking once win.
        #undo(board,action)
    print(f'v_prev maxi = {v_prev}')
    return v_prev