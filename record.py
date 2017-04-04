from es import EvolutionStrategy
import numpy as np
from game import Game, play
from os import path
import os
import json

es = EvolutionStrategy(fn=play, noisep=50, sigma=0.1, alpha=0.001, layer_sizes=[[4, 500], [500, 1]], input_size=4)
load = path.join(path.dirname(__file__), 'load.npy')

# if load.npy exists, load the parameters from it
if path.exists(load):
    es.layers = np.load(load)

states = play(es.forward, record=True)

print(json.dumps(states))

