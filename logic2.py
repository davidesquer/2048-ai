import numpy as np
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

def move_board(board, direction):
    new_board = np.copy(board)
    moved = False
    
    if direction == Direction.UP or direction == Direction.DOWN:
        new_board = new_board.T
    
    if direction == Direction.DOWN or direction == Direction.RIGHT:
        new_board = np.flip(new_board, axis=1)

    for row in range(new_board.shape[0]):
        non_zeros = new_board[row, new_board[row] != 0]
        merged = []

        i = 0
        while i < len(non_zeros):
            if i < len(non_zeros) - 1 and non_zeros[i] == non_zeros[i + 1]:
                merged.append(2 * non_zeros[i])
                i += 1
            else:
                merged.append(non_zeros[i])
            i += 1

        while len(merged) < new_board.shape[1]:
            merged.append(0)

        if not np.array_equal(new_board[row], merged):
            moved = True

        new_board[row] = merged

    if direction == Direction.DOWN or direction == Direction.RIGHT:
        new_board = np.flip(new_board, axis=1)

    if direction == Direction.UP or direction == Direction.DOWN:
        new_board = new_board.T

    return moved, new_board

def expand_node(node):
    children = []
    
    for direction in Direction:
        moved, new_board = move_board(node.state, direction)
        
        if moved:
            child = Node(new_board, parent=node, move=direction)
            children.append(child)
    
    return children

def heuristic(state):
    return (np.max(state)*2) + (np.sum(board == 0)**2) + np.sum(state)

def dls(current_node, depth):
    if depth == 0:
        return heuristic(current_node.state), current_node.move

    best_score = -1
    best_move = None

    if depth > 0:
        for child in expand_node(current_node):
            score, move = dls(child, depth - 1)
            
            if score > best_score:
                best_score = score
                best_move = move if current_node.move is None else current_node.move

    return best_score, best_move

def iddfs(board, max_depth):
    root = Node(board)
    best_move = None
    best_score = -1
    
    for depth in range(max_depth):
        score, move = dls(root, depth)
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move