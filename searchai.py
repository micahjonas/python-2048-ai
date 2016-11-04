import random
import game
import math

DEPTH_LIMIT = 3
LOW_PROBABILITY = 0.0000001

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

    if board == newboard:
        print board
        print newboard
        print 'why?'
        return 0

    return score_tilechoose_node(depth, newboard, 1)

def score_tilechoose_node(depth, board, prob):
    if depth > DEPTH_LIMIT or prob < LOW_PROBABILITY:
        print depth
        return score_board(board)


    empty_positions = []
    res = 0

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:
                empty_positions.append((y,x))

    prob = prob / len(empty_positions)

    for position in empty_positions:
        y,x = position
        newboard = board
        newboard[y][x]=2
        res += score_move_node(depth, newboard, prob*0.9)
        newboard[y][x]=4
        res += score_move_node(depth, newboard, prob*0.1)

    return res


def score_board(b):
    """
    Returns the heuristic value of b
    Snake refers to the "snake line pattern" (http://tinyurl.com/l9bstk6)
    Here we only evaluate one direction; we award more points if high valued tiles
    occur along this path. We penalize the board for not having
    the highest valued tile in the lower left corner
    """
    return gradientUtility(b)
    """snake = []
    for i, col in enumerate(zip(*b)):
        snake.extend(reversed(col) if i % 2 == 0 else col)

    m = max(snake)
    print 'rate board'
    print b
    res = sum(x/10**n for n, x in enumerate(snake)) - \
           math.pow((b[3][0] != m)*abs(b[3][0] - m), 2)
    print res
    return res
    #sys.exit("Not implemented")"""


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
        return game.merge_right
    else:
        sys.exit("No valid move")


'''
Grid.prototype.monotonicity = function() {
 var monoScores = [0, 0, 0, 0];

  for (var i=0; i<4; i++) {
    var current = 0;
    var next = current+1;
    while ( next<4 ) {
      while ( next<4 && !this.cellOccupied({x: i, y: next})) {
        next++;
      }
      if (next>=4) { next--; }
      var currentValue = this.cellOccupied({x:i, y:current}) ?
        Math.log(this.cellContent( this.cells[i][current] ).value) / Math.log(2) :
        0;
      var nextValue = this.cellOccupied({x:i, y:next}) ?
        Math.log(this.cellContent( this.cells[i][next] ).value) / Math.log(2) :
        0;
      if (currentValue > nextValue) {
        monoScores[0] += nextValue - currentValue;
      } else if (nextValue > currentValue) {
        monoScores[1] += currentValue - nextValue;
      }
      current = next;
      next++;
    }
  }

  for (var j=0; j<4; j++) {
    var current = 0;
    var next = current+1;
    while ( next<4 ) {
      while ( next<4 && !this.cellOccupied({x:next, y:j})) {
        next++;
      }
      if (next>=4) { next--; }
      var currentValue = this.cellOccupied({x:current, y:j}) ?
        Math.log(this.cellContent( this.cells[current][j] ).value) / Math.log(2) :
        0;
      var nextValue = this.cellOccupied({x:next, y:j}) ?
        Math.log(this.cellContent( this.cells[next][j] ).value) / Math.log(2) :
        0;
      if (currentValue > nextValue) {
        monoScores[2] += nextValue - currentValue;
      } else if (nextValue > currentValue) {
        monoScores[3] += currentValue - nextValue;
      }
      current = next;
      next++;
    }
  }

  return Math.max(monoScores[0], monoScores[1]) + Math.max(monoScores[2], monoScores[3]);
}

'''
def gradientUtility(board):
    gradients = [[[ 3, 2, 1, 0],[ 2, 1, 0,-1],[ 1, 0,-1,-2],[ 0,-1,-2,-3]],
                 [[ 0, 1, 2, 3],[-1, 0, 1, 2],[-2,-1, 0, 1],[-3,-2,-1,-0]],
                 [[ 0,-1,-2,-3],[ 1, 0,-1,-2],[ 2, 1, 0,-1],[ 0,-1,-2,-3]],
                 [[-3,-2,-1, 0],[-2,-1, 0, 1],[-1, 0, 1, 2],[ 0, 1, 2, 3]]]

    values = [0,0,0,0]

    for i in range(4):
        for y in range(4):
            for x in range(4):
                if board[y][x] > 0:
                    values[i] += gradients[i][x][y] * board[y][x]

    return max(values)
'''


  for (var i = 0; i < 4; i++) {
    this.eachCell(function(x, y, tile) {
      if (tile)
        values[i] += gradients[i][x][y] * tile.value;
    });
  }
  return Math.max.apply(Math, values);
}'''
