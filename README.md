pip modules: websocket-client

## Running the browser-control version

### Firefox

Install [Remote Control for Firefox](https://github.com/nneonneo/FF-Remote-Control/raw/V_1.2/remote_control-1.2-fx.xpi).

Open up the [2048 game](http://gabrielecirulli.github.io/2048/) or any compatible clone and start remote control.

Run `python 2048.py -b firefox` and watch the game!

### Chrome

Enable Chrome remote debugging by starting it with the `remote-debugging-port` command-line switch (e.g. `google-chrome --remote-debugging-port=9222`).


Windows:???
OS X: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`

Open up the [2048 game](http://gabrielecirulli.github.io/2048/), then run `python 2048.py -b chrome` and watch the game! The `-p` option can be used to set the port to connect to.
