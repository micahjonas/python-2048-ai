# Sample 2048 Search AI implementation

Simple framework to learn about expectimax search and utility for 2048.

  * game.py contains a simple set of functions to merge a board for simulation purposes
  * searchai.py is where the magic happens
    * find_best_move(board) gets a game state and searches for the optimal move
    * score_board(board) get a board and tries to figure out it's future value

A board is a nested array which represents the board. [[0,0,0,0],[1,2,0,0],[3,0,0,2],[0,0,0,0]]
For the sake of convenience the tiles are represented by the log2 of the tile value.
(Can be changed in gmaectrl.py in the get_board function.)

For further reference:
 * https://github.com/nneonneo/2048-ai
 * http://gjdanis.github.io/2015/09/27/2048-game-and-ai/



## Chrome (tested for OS X & Chrome)

Enable Chrome remote debugging by starting it with the `remote-debugging-port` command-line switch (e.g. `google-chrome --remote-debugging-port=9222`).

Windows:???
OS X: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`

Open up the [2048 game](http://gabrielecirulli.github.io/2048/), then run `python 2048.py -b chrome` and watch the game! The `-p` option can be used to set the port to connect to.

## Firefox

Install [Remote Control for Firefox](https://github.com/nneonneo/FF-Remote-Control/raw/V_1.2/remote_control-1.2-fx.xpi).

Open up the [2048 game](http://gabrielecirulli.github.io/2048/) or any compatible clone and start remote control.

Run `python 2048.py -b firefox` and watch the game!
