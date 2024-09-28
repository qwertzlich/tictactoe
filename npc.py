''' This module contains the implementation of the minimax algorithm for the game of tic-tac-toe. The first player is represented by 1, the second player by -1.'''
import numpy as np
from numpy.typing import NDArray

def players(state : NDArray[np.int32]) -> int:
    '''Given a state returns whose turn it is'''
    if np.count_nonzero(state) % 2 == 0:
        return 1
    return -1 #1 starts the game

def actions(state : NDArray[np.int32]) -> NDArray[np.int32]:
    '''Given a state returns the set of all legal actions in that state'''
    return np.argwhere(state == 0)

def result(state : NDArray, action : NDArray) -> NDArray:
    '''Given a state and an action, returns the resulting state'''
    player = players(state)
    new_state = state.copy()
    new_state[action[0], action[1]] = player
    return new_state

def terminal_util(state : NDArray) -> tuple:
    '''Given a state, returns whether the game is over and the utility of the state'''
    diag, offdiag = (np.diagonal(state), np.fliplr(state).diagonal())
    if sum(diag) == 3 or sum(offdiag) == 3:
        return (True, 1)
    if sum(diag) == -3 or sum(offdiag) == -3:
        return (True, -1)
    for i in range(3):
        if sum(state[:, i]) == 3 or sum(state[i, :]) == 3:
            return (True, 1)
        if sum(state[:, i]) == -3 or sum(state[i, :]) == -3:
            return (True, -1)
    if np.count_nonzero(state) == 9:
        return (True, 0)
    return (False, None)

def max_value(state : NDArray) -> NDArray:
    '''Given a state, returns the best value of that state for the max player'''
    is_terminal, utility = terminal_util(state)
    if is_terminal:
        return utility
    v = -np.inf
    for a in actions(state):
        v = max(v, min_value(result(state, a)))
    return v

def min_value(state : NDArray) -> NDArray:
    '''Given a state, returns the best value of that state for the min player'''
    is_terminal, utility = terminal_util(state)
    if is_terminal:
        return utility
    v = np.inf
    for a in actions(state):
        v = min(v, max_value(result(state, a)))
    return v

def minimax(state : NDArray) -> NDArray:
    '''Given a state, returns the best action for the current player'''
    if players(state) == 1:
        v = -np.inf
        for a in actions(state):
            u = min_value(result(state, a))
            if u > v:
                v = u
                action = a
    else:
        v = np.inf
        for a in actions(state):
            u = max_value(result(state, a))
            if u < v:
                v = u
                action = a
    return action

# board = np.array([[1, -1, 0],
#                   [-1, -1, 1],
#                   [1, 1, 0]])

# print(minimax(board)) # Expected output: [2, 1]