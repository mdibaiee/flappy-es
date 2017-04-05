Playing Flappy Bird using Evolution Strategies
==============================================

After reading [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://blog.openai.com/evolution-strategies/), I wanted to experiment something using Evolution Strategies, and Flappy Bird has always been one of my favorites when it comes to Game experiments. A simple yet challenging game.

The model learns to play very well after 3000 epochs, but not completely flawless and it rarely loses in difficult cases (high difference between two wall entrances).
Training process is pretty fast as there is no backpropagation, and is not very costy in terms of memory as there is no need to record actions as in policy gradients.

Here is a demonstration of the model after 3000 epochs (~5 minutes on an Intel(R) Core(TM) i7-4770HQ CPU @ 2.20GHz):

![after training](/demo/flappy-success.gif)

also see: [Before training](/demo/flappy-lose.gif)

There is also a [a web version](http://labs.aylien.com/flappy-bird) available for ease of access.

For each frame the bird stays alive, +0.1 score is given to him. For each wall he passes, +10 score is given.

Try it yourself
---------------
You need python3 and pip for installing and running the code.

First, install dependencies (you might want to create a [virtualenv](https://virtualenv.pypa.io)):

```
pip install -r requirements
```

The pretrained parameters are in a file named `load.npy` and will be loaded when you run `train.py` or `demo.py`.

`train.py` will train the model, saving the parameters to `saves/<TIMESTAMP>/save-<ITERATION>`.

`demo.py` shows the game in a GTK window so you can see how the AI actually plays (like the GIF above).

`play.py` if you feel like playing the game yourself, space: jump, once lost, press enter to play again. :grin:

_pro tip: reach 100 score and you will become THUG FOR LIFE :smoking:_

Notes
-----

It seems training past a maximum point reduces performance, learning rate decay might help with that.
My interpretation is that after finding a local maximum for accumulated reward and being able to receive high rewards,
the updates become pretty large and will pull the model too much to sides, thus the model will enter a state of oscillation.

To try it yourself, there is a `long.npy` file, rename it to `load.npy` (backup `load.npy` before doing so) and run `demo.py`,
you will see the bird failing more often than not. `long.py` was trained for only 100 more epochs than `load.npy`.
