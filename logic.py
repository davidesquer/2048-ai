import numpy as np
import random
from copy import deepcopy
import concurrent.futures

def start_2048():
    board = np.zeros((4, 4), dtype=int)

    for _ in range(2):
        spawn_tile(board)

    return board

def spawn_tile(board, tile_value=None):
    empty_cells = list(zip(*np.where(board == 0)))
    if not empty_cells:
        return board
    
    if tile_value is None:
        tile_value = 2 if random.random() < 0.9 else 4

    row, col = random.choice(empty_cells)
    board[row, col] = tile_value
    return board

def move_board(board, move):
    moved = False

    if move in ["up", "down"]:
        board = board.T

    for row in range(4):
        if move in ["right", "down"]:
            board[row] = board[row][::-1]

        moved_row, row_changed = move_row(board[row])
        board[row] = moved_row

        if not moved and row_changed:
            moved = True

        if move in ["right", "down"]:
            board[row] = board[row][::-1]

    if move in ["up", "down"]:
        board = board.T

    return board, moved

def move_row(row):
    non_zeros = row[row != 0]
    new_row = np.zeros_like(row)

    i = 0
    skip = False
    for j in range(len(non_zeros)):
        if skip:
            skip = False
            continue

        if j < len(non_zeros) - 1 and non_zeros[j] == non_zeros[j + 1]:
            new_row[i] = non_zeros[j] * 2
            skip = True
        else:
            new_row[i] = non_zeros[j]

        i += 1

    return new_row, not np.array_equal(new_row, row)

def is_game_over(board):
    if not np.any(board == 0):
        for move in ["up", "down", "left", "right"]:
            temp_board, moved = move_board(board.copy(), move)
            if moved:
                return False
        return True
    return False

def make_move(board, move):
    if move not in ["up", "down", "left", "right"]:
        print("Invalid move. Please enter up, down, left, or right.")
        return None

    new_board, moved = move_board(board.copy(), move)

    if not moved:
        print("Invalid move. No change in board.")
        return None

    spawn_tile(new_board)
    game_over = is_game_over(new_board)

    if game_over:
        print("Game over! Final board:")
        print(new_board)
        return None

    return new_board

def get_corner_values(array):
    if array.ndim != 2:
        raise ValueError("Only 2D arrays are supported.")
    
    rows, cols = array.shape
    top_left = array[0, 0]
    top_right = array[0, cols-1]
    bottom_left = array[rows-1, 0]
    bottom_right = array[rows-1, cols-1]
    
    return np.array([top_left, top_right, bottom_left, bottom_right]).max()

def score_board(board):
    # A simple heuristic to score the board based on the highest tile and number of empty cells
    highest_tile = np.max(board)
    empty_cells = np.sum(board == 0)
    int_board = np.array(board)
    
    if (np.max(board) == get_corner_values(int_board)):
        extra_value = int_board.max() * 5
    else:
        extra_value = -int_board.max()
    
    return highest_tile + (empty_cells**3) + extra_value

def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or is_game_over(board):
        return score_board(board)

    if maximizing_player:
        max_value = float('-inf')
        for move in ["up", "down", "left", "right"]:
            new_board, moved = move_board(deepcopy(board), move)
            if moved:
                value = minimax(new_board, depth - 1, False, alpha, beta)
                max_value = max(max_value, value)
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
        return max_value
    else:
        min_value = float('inf')
        new_boards = [spawn_tile(deepcopy(board), tile_value=2), spawn_tile(deepcopy(board), tile_value=4)]
        for new_board in new_boards:
            value = minimax(new_board, depth - 1, True, alpha, beta)
            min_value = min(min_value, value)
            beta = min(beta, min_value)
            if beta <= alpha:
                break
        return min_value

def best_move_helper(args):
    move, board, depth = args
    new_board, moved = move_board(deepcopy(board), move)
    if moved:
        value = minimax(new_board, depth - 1, False, float('-inf'), float('inf'))
        return value, move
    return float('-inf'), None

def best_move(board, depth):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        moves = ["up", "down", "left", "right"]
        args = [(move, board, depth) for move in moves]
        results = list(executor.map(best_move_helper, args))

    best_value, best_move = max(results, key=lambda x: x[0])
    return best_move