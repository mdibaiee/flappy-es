from es import EvolutionStrategy
import numpy as np
from game import Game, play
from win import Window, GAME_SPEED
import gi
from gi.repository import Gtk, GLib, Gdk
from datetime import datetime
from os import path
import os
from draw_chart import draw_chart

es = EvolutionStrategy(fn=play, noisep=50, sigma=0.1, alpha=0.001, layer_sizes=[[4, 500], [500, 1]], input_size=4)
load = path.join(path.dirname(__file__), 'load.npy')

np.random.seed(0)

# if load.npy exists, load the parameters from it
if path.exists(load) and not os.environ.get('SKIP_LOAD'):
    es.layers = np.load(load)

# show the game every n iterations
SHOW_EVERY = int(os.environ.get('SHOW_EVERY', 100))
# save the parameters every n iterations
SAVE_EVERY = int(os.environ.get('SAVE_EVERY', 100))
# number of steps
STEPS = int(os.environ.get('STEPS', 10000))

# an id for saving the parameters in a folder
run_id = str(datetime.now())
print("run {}".format(run_id))
os.mkdir(path.join(path.dirname(__file__), 'saves', run_id))

# this function is called when showing the game to user
def step(game, update):
    win = Window(game)
    GLib.timeout_add(GAME_SPEED, lambda: timeout_kill(win, game))
    GLib.timeout_add(GAME_SPEED, update)
    GLib.timeout_add(GAME_SPEED, win.update)
    win.show_all()
    Gtk.main()

# once the bird has lost, kill the window and stop Gtk loop
def timeout_kill(win, game):
    if game.lost:
        Gtk.main_quit()
        win.destroy()
        return False
    
    return True

reward_scatter_x = []
reward_scatter_y = []

reward_line_x = list(range(STEPS))
reward_line_y = []

for i in range(STEPS):
    print("{}: ".format(i), end='')
    rewards = es.train()
    m = np.mean(rewards)

    reward_line_y.append(m)

    for r in rewards:
        reward_scatter_x.append(i)
        reward_scatter_y.append(r)

    if SHOW_EVERY and i % SHOW_EVERY == 0:
        play(es.forward, step=step)
        Gtk.main_quit()
        print(' shown')
    else:
        score = play(es.forward)
        print(' score: {:.2f}'.format(score))

    if i % SAVE_EVERY == 0:
        p = path.join(path.dirname(__file__), 'saves', run_id, 'save-{}'.format(i))
        np.save(p, es.layers)
        draw_chart(reward_scatter_x, reward_scatter_y, reward_line_x, reward_line_y)
