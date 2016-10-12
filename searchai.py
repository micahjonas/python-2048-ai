import random

def find_best_move(board):
    best = 0
    bestmove = -1

    for move in range(0,3):
        res = score_toplevel_move(board, move)

        if res > best:
            best = res
            bestmove = move

    return bestmove

# use eval state?
# transposition table
# current depth
# cachehits
# moves evaled
# depth limit

def score_toplevel_move(board, move):
    # set depth limit fix? variable?
    # depth_limit max(3, count_distinct_tiles(board) -2)
    depth_limit = 3

    return _score_toplevel_move(depth_limit, board, move)

def _score_toplevel_move(depth, board, move):

    newboard = execute_move(move, board)

    if(board == newboard)
        return 0

    return score_tilechoose_node(depth, newboard, 1)

def score_tilechoose_node(depth, board, porb):
    if depth >= DEPTH_LIMIT or prob < LOW_PROBABILITY
        return score_board(board)

    prob = prob / count_empty(board)

    res = 0

    #fill every empty field with 2 or 4




def score_move_node(depth, board, prob):
    depth = depth + 1
    best = 0
    for move in range(0,3):
        newboard = execute_move(move, board)

        if (board != newboard):
            best = max(best, score_tilechoose_node(depth, newboard, prob))

    return best
