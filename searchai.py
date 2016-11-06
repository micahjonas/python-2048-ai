import random
import game
import math

DEPTH_LIMIT = 4
LOW_PROBABILITY = 0.0000000000000000000000000000001

def find_best_move(board):
    best = 0
    bestmove = -1

    print ' '
    for move in range(4):
        res = score_toplevel_move(board, move)
        print move
        print res
        if res > best:
            best = res
            bestmove = move

    print ' '
    return bestmove

def score_toplevel_move(board, move):
    # set depth limit fix? variable?
    # depth_limit max(3, count_distinct_tiles(board) -2)

    newboard = execute_move(move, board)

    if board == newboard:
        return 0

    depth = 1
    prob = 1

    return score_tilechoose_node(depth, newboard, prob)


def score_tilechoose_node(depth, board, prob):
    if depth > DEPTH_LIMIT or prob < LOW_PROBABILITY:
        return score_board(board)

    empty_positions = []
    res = 0

    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                empty_positions.append((y,x))


    prob = prob / len(empty_positions)

    for position in empty_positions:
        y,x = position
        newboard = board
        newboard[y][x]=1
        res += score_move_node(depth, newboard, prob*0.9)
        newboard[y][x]=2
        res += score_move_node(depth, newboard, prob*0.1)

    return res


def score_board(board):

    empty = empty_tiles_utility(board)
    gradient = gradient_utility(board)
    mono =  monotonicity_utility(board)

    #score = score_utility(board)

    return 10*gradient + mono + 100*empty


def score_move_node(depth, board, prob):
    depth = depth + 1
    best = 0
    for move in range(0,3):
        newboard = execute_move(move, board)

        if (board != newboard):
            best = max(best, score_tilechoose_node(depth, newboard, prob))

    return best


def execute_move(move, board):
    """
    move and return the grid
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")

def score_utility(board):
    '''
    Calculate board value, with higher prio for higher tiles
    '''
    summed_value = 0
    for row in board:
        for value in row:
            summed_value = summed_value + math.pow(value, 3)

    return summed_value

def empty_tiles_utility(board):
    '''
    Count number of emtpy tiles
    '''
    empty_tiles = 0
    for row in board:
        for value in row:
            if value == 0:
                empty_tiles = empty_tiles + 1

    return empty_tiles


def monotonicity_utility(board):
    monoScores = [0, 0, 0, 0]

    for i in range(4):
        currentTile = 0
        nextTile = currentTile + 1

        while nextTile < 4:
            while nextTile < 4 and board[i][nextTile] > 0:
                nextTile = nextTile + 1
            if nextTile >= 4:
                nextTile = nextTile - 1
            currentValue = board[i][currentTile]
            nextValue = board[i][nextTile]
            if currentValue > nextValue:
                monoScores[0] += nextValue - currentValue
            elif nextValue > currentValue:
                monoScores[1] += currentValue - nextValue
            currentTile = nextTile
            nextTile = nextTile + 1

    for i in range(4):
        currentTile = 0
        nextTile = currentTile + 1

        while nextTile < 4:
            while nextTile < 4 and board[nextTile][i] > 0:
                nextTile = nextTile + 1
            if nextTile >= 4:
                nextTile = nextTile - 1
            currentValue = board[currentTile][i]
            nextValue = board[nextTile][i]
            if currentValue > nextValue:
                monoScores[2] += nextValue - currentValue
            elif nextValue > currentValue:
                monoScores[3] += currentValue - nextValue
            currentTile = nextTile
            nextTile = nextTile + 1

    return max(monoScores[0], monoScores[1]) + max(monoScores[2], monoScores[3])


def gradient_utility(board):
    '''
    Values board position after a gradients.
    Which in practical use means we want higher numbered tiles in the corners
    and increase from there.
    The values are raised to the power of 3 instead of 2 to emphazise that higher
    tiles are more valued
    '''
    gradients = [[[ 3, 2, 1, 0],[ 2, 1, 0,-1],[ 1, 0,-1,-2],[ 0,-1,-2,-3]],
                 [[ 0, 1, 2, 3],[-1, 0, 1, 2],[-2,-1, 0, 1],[-3,-2,-1,-0]],
                 [[ 0,-1,-2,-3],[ 1, 0,-1,-2],[ 2, 1, 0,-1],[ 0,-1,-2,-3]],
                 [[-3,-2,-1, 0],[-2,-1, 0, 1],[-1, 0, 1, 2],[ 0, 1, 2, 3]]]

    values = [0,0,0,0]

    for i in range(4):
        for y in range(4):
            for x in range(4):
                if board[y][x] > 0:
                    values[i] += gradients[i][x][y] * pow(board[y][x],3)

    return max(values)
