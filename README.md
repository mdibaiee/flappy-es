Playing Flappy Bird using Evolution Strategies
==============================================

After reading [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://blog.openai.com/evolution-strategies/), I wanted to experiment something using Evolution Strategies, and Flappy Bird has always been one of my favorites when it comes to Game experiments. A simple yet challenging game.

The model learns to play very well after ~1500 iterations, but not completely flawless and it usually loses in difficult cases (high difference between two wall entrances).
Training process is pretty fast as there is no backpropagation, and is not very costy in terms of memory as there is no need to record actions as in policy gradients.

Here is a demonstration of the model before training and after ~3000 iterations (less than an hour of training):

Before training:

![before training](/demo/flappy-lose.gif)
![after training](/demo/flappy-success.gif)

For each frame the bird stays alive, +1 score is given to him. For each wall he passes, +10 score is given.

Try it yourself
---------------
First, install dependencies:

```
pip install -r requirements
```

The pretrained parameters are in a file named `load.npy` and will be loaded when you run `train.py` or `demo.py`.

`train.py` will train the model, saving the parameters to `saves/<TIMESTAMP>/save-<ITERATION>`.

`demo.py` shows the game in a GTK window so you can see how the AI actually plays.

`play.py` if you feel like playing the game yourself, space: jump, once lost, press enter to play again. :grin:
_pro tip: reach 100 score and you will become THUG FOR LIFE :smoking:_

Notes
-----

It seems training for too long reduces the performance after a while, learning rate decay might help with that.
To try it yourself, there is a `long.npy` file, rename it to `load.npy` (backup `load.npy` before doing so) and run `demo.py`,
you will see the bird failing more often than not. `long.py` was trained for ~2000 more iterations than `load.npy`.
