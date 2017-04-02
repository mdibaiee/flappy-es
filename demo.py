from es import EvolutionStrategy
import numpy as np
from game import Game, play
from win import Window, GAME_SPEED
import gi
from gi.repository import Gtk, GLib, Gdk
from os import path
import os
import time

es = EvolutionStrategy(fn=play, noisep=50, sigma=0.1, alpha=0.001, layer_sizes=[[4, 500], [500, 1]], input_size=4)
load = path.join(path.dirname(__file__), 'load.npy')

# if load.npy exists, load the parameters from it
if path.exists(load):
    es.layers = np.load(load)

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

time.sleep(5)

for i in range(10000):
    play(es.forward, step=step)
    Gtk.main_quit()
