# -*- coding: UTF-8 -*-
import random
import numpy as np

# PY3 compat
try:
    xrange
except NameError:
    xrange = range


class Game(object):
    """
    A 2048 board
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    SIZE = 4

    def __init__(self, size=SIZE, **kws):
        self.__size = size
        self.__size_range = xrange(0, self.__size)
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()
        self.score = 0
        self.nomove = 0

    def size(self):
        """return the board size"""
        return self.__size

    def score(self):
        """return the score"""
        return self.score

    def nomove(self):
        """return the score"""
        return self.nomove

    def canMove(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in self.__size_range:
            for x in self.__size_range:
                c = self.getCell(x, y)
                if (x < self.__size-1 and c == self.getCell(x+1, y)) \
                   or (y < self.__size-1 and c == self.getCell(x, y+1)):
                    return True

        return False

    def filled(self):
        """
        return true if the game is filled
        """
        return len(self.getEmptyCells()) == 0

    def addTile(self, value=None, choices=([2]*9+[4])):
        """
        add a random tile in an empty cell
          value: value of the tile to add.
          choices: a list of possible choices for the value of the tile.
                   default is [2, 2, 2, 2, 2, 2, 2, 2, 2, 4].
        """
        if value:
            choices = [value]

        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCells(self):
        """return all the cells"""
        return self.cells

    def __transform(self, number):
        if number == 0:
            return 0
        else:
            return int(np.log2(number))

    def getCellsLog2(self):
        nparr = np.array(self.cells)
        nparr = np.log2(nparr)
        nparr[np.isneginf(nparr)] = 0
        return nparr.astype("uint8")
        #return [[self.__transform(x) for x in line] for line in self.cells]

    def getCell(self, x, y):
        """return the cell value at x,y"""
        return self.cells[y][x]

    def setCell(self, x, y, v):
        """set the cell value at x,y"""
        self.cells[y][x] = v

    def getLine(self, y):
        """return the y-th line, starting at 0"""
        return self.cells[y]

    def getCol(self, x):
        """return the x-th column, starting at 0"""
        return [self.getCell(x, i) for i in self.__size_range]

    def setLine(self, y, l):
        """set the y-th line, starting at 0"""
        self.cells[y] = l[:]

    def setCol(self, x, l):
        """set the x-th column, starting at 0"""
        for i in xrange(0, self.__size):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """return a (x, y) pair for each empty cell"""
        return [(x, y)
                for x in self.__size_range
                for y in self.__size_range if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == Game.LEFT or d == Game.UP):
            inc = 1
            rg = xrange(0, self.__size-1, inc)
        else:
            inc = -1
            rg = xrange(self.__size-1, 0, inc)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+inc]:
                v = line[i]*2
                line[i] = v
                line[i+inc] = 0
                pts += v

        return (line, pts)

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Game.UP or d == Game.LEFT:
            return nl + [0] * (self.__size - len(nl))
        return [0] * (self.__size - len(nl)) + nl

    def getGrid(self):
        """
        Returns the grid
        """
        return sefl.cells

    def getActionSet(self):
        return [0,1,2,3]

    def reset(self):
        self.__size = Game.SIZE
        self.__size_range = xrange(0, self.__size)
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()
        self.score = 0
        self.nomove = 0

    def move(self, d, add_tile=True):
        """
        move and return the grid
        """
        if d == Game.LEFT or d == Game.RIGHT:
            chg, get = self.setLine, self.getLine
        elif d == Game.UP or d == Game.DOWN:
            chg, get = self.setCol, self.getCol
        else:
            return self.cells

        moved = False
        scoreOfRound = 0

        for i in self.__size_range:
            # save the original line/col
            origin = get(i)
            # move it
            line = self.__moveLineOrCol(origin, d)
            # merge adjacent tiles
            collapsed, pts = self.__collapseLineOrCol(line, d)
            # move it again (for when tiles are merged, because empty cells are
            # inserted in the middle of the line/col)
            new = self.__moveLineOrCol(collapsed, d)
            # set it back in the board
            chg(i, new)
            # did it change?
            if origin != new:
                moved = True
                self.nomove += 1
            scoreOfRound += pts

        self.score += scoreOfRound

        # don't add a new tile if nothing changed
        if moved and add_tile:
            self.addTile()

        return scoreOfRound

    def cellsToString(self, cells):
        res = ""
        for line in cells:
            res += " ".join(map(str, line))
            res += "\n"

        return


def merge_right(b):
    """
    Merge the board right
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> merge_right(test)
    [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    """

    def reverse(x):
        return list(reversed(x))

    t = map(reverse, b)
    return [reverse(x) for x in merge_left(t)]

def merge_up(b):
    """
    Merge the board upward. Note that zip(*t) is the
    transpose of b
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> merge_up(test)
    [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    """

    t = merge_left(zip(*b))
    return [list(x) for x in zip(*t)]

def merge_down(b):
    """
    Merge the board downward. Note that zip(*t) is the
    transpose of b
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> merge_down(test)
    [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    """

    t = merge_right(zip(*b))
    return [list(x) for x in zip(*t)]

def merge_left(b):
    """
    Merge the board left
    Args: b (list) two dimensional board to merge
    Returns: list
    """

    def merge(row, acc):
        """
        Recursive helper for merge_left. If we're finished with the list,
        nothing to do; return the accumulator. Otherwise, if we have
        more than one element, combine results of first from the left with right if
        they match. If there's only one element, no merge exists and we can just
        add it to the accumulator.
        Args:
            row (list) row in b we're trying to merge
            acc (list) current working merged row
        Returns: list
        """

        if not row:
            return acc

        x = row[0]
        if len(row) == 1:
            return acc + [x]

        return merge(row[2:], acc + [2*x]) if x == row[1] else merge(row[1:], acc + [x])

    board = []
    for row in b:
        merged = merge([x for x in row if x != 0], [])
        merged = merged + [0]*(len(row)-len(merged))
        board.append(merged)
    return board

def move_exists(b):
    """
    Check whether or not a move exists on the board
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    >>> move_exists(b)
    False
    >>> move_exists(test)
    True
    """
    for row in b:
        for x, y in zip(row[:-1], row[1:]):
            if x == y or x == 0 or y == 0:
                return True
    return False
