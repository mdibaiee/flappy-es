import numpy as np
import random
from copy import copy

GRAVITY = 2
FRICTION = 0.9
class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bird = Bird(width / 2, height / 2)
        self.wall = self.create_wall()
        self.lost = False
        self.score = 0;
        self.record = False

        self.states = []

    def update(self):
        self.bird.update()
        self.wall.update()

        # 10 score for passing a wall
        if (self.wall.x + self.wall.width) < self.width / 2:
            self.wall = self.create_wall()
            self.score += 10
            if not self.record:
                print("\033[32m+\033[0m", end='')

        if self.intercept(self.bird, self.wall):
            self.lost = True

        if self.bird.y < 0 or self.bird.y > self.height:
            self.lost = True

        # a constant score for each movement, this way
        # our birds will try to stay alive longer and
        # our evolution strategy won't start with zero reward
        self.score += 0.1

        if self.record:
            rec = { 'width': self.width,
                    'height': self.height,
                    'lost': self.lost,
                    'score': round(self.score, 2),
                    

                    'bird': {
                        'x': self.bird.x,
                        'y': self.bird.y,
                    },

                    'wall': {
                        'x': self.wall.x,
                        'gate': {
                            'y': self.wall.gate.y,
                            'height': self.wall.gate.height
                        }
                    }
                }
            self.states.append(rec)

    # create a wall, the wall is between the 15%-65% of the screen
    def create_wall(self):
        return Wall(self.width - WALL_WIDTH, self.height * (0.15 + np.random.random() * 0.5) )
        
    def intercept(self, bird, wall):
        return ((bird.x + bird.width) > wall.x and
                ((bird.y + bird.height) > (wall.gate.y + wall.gate.height) or
                 (bird.y) < wall.gate.y))

JUMP_STEPS = 2
JUMP_SPEED = 7
class Bird():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 18

        self.velocity = np.array([0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0], dtype=np.float64)

    def jump(self):
        self.velocity[1] = -JUMP_SPEED
        self.acceleration[1] = 0

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.velocity += self.acceleration
        self.velocity *= FRICTION

        self.acceleration[1] = GRAVITY

WALL_WIDTH = 30
GATE_HEIGHT = 60
class Wall():
    def __init__(self, x, y):
        self.x = x

        self.gate = dotdict({
            'y': y,
            'height': GATE_HEIGHT
        })

        self.width = WALL_WIDTH

    def update(self):
        self.x -= 2

class dotdict(dict):
  """dot.notation access to dictionary attributes"""
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

# limit the game to 1000 frames while training, sometimes a game might take
# too long to finish after a while of training
MAX_FRAMES = 10000
def play(fn, step=None, record=False):
    game = Game(250, 200)
    frame = 0

    # while showing to user, we want to update the GTK frontend
    # the `step` function is responsible for doing just that, see index.py
    if step:
        return step(game, lambda: show_update(fn, game))

    if record:
        game.record = True

    while not game.lost and frame < MAX_FRAMES:
        frame += 1
        # input of the model: bird x, bird y, distance to next wall, height of wall's entrance
        data = np.array([[game.bird.x, game.bird.y, game.bird.x - game.wall.x, game.wall.gate.y]])
        jump = fn(data)[0][0]

        if jump > 0.5:
            game.bird.jump()

        game.update()

    if record:
        return game.states

    return game.score

def show_update(fn, game):
    if not game.lost:
        data = np.array([[game.bird.x, game.bird.y, game.bird.x - game.wall.x, game.wall.gate.y]])
        jump = fn(data)[0][0]

        if jump > 0.5:
            game.bird.jump()

        game.update()
        return True
    else:
        return False

