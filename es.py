import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class EvolutionStrategy():
    # fn: function that plays the game and returns the rewards, this function must take as argument another function that
    #     determines whether the bird should jump or not
    #     e.g. def fn shouldJump = if shouldJump(some_input): ... return reward
    # noisep: noise population, how many different noises should be tried at each step
    # sigma: standard deviation of generated noise
    # alpha: learning rate
    # layer_sizes: sizes of neural network layers, e.g. [[4, 500], [500, 1]]
    # input_size: number of inputs
    def __init__(self, fn, noisep, sigma, alpha, layer_sizes, input_size):
        self.fn = fn

        self.sigma = sigma
        self.noisep = noisep
        self.alpha = alpha
        self.layer_sizes = layer_sizes
        self.input_size = input_size

        # initialize layers randomly
        self.layers = []
        for i, layer in enumerate(layer_sizes):
            self.layers.append(np.random.uniform(-0.1, 0.1, layer))

    # forward propagation: sigmoid(xW) for every layer
    def forward(self, input):
        output = input
        for i, layer in enumerate(self.layers):
            output = sigmoid(np.dot(output, layer))

        return output
        
    # train the model
    def train(self):
        N = [[] for i in range(len(self.layers))]
        R = np.zeros(self.noisep)

        for i in range(self.noisep):
            noisy_layers = []

            for j, (layer_size, layer) in enumerate(zip(self.layer_sizes, self.layers)):
                # for each layer, generate a noise
                n = np.random.randn(*layer_size)
                N[j].append(n)

                # add noise to layer
                noisy_w = layer + self.sigma * n

                noisy_layers.append(noisy_w)

            # generate another network with the same parameters, but with noisy layers
            es = EvolutionStrategy(fn=self.fn, noisep=self.noisep, sigma=self.sigma, alpha=self.alpha, layer_sizes=self.layer_sizes, input_size=self.input_size)

            es.layers = noisy_layers
            # run a forward propagation using the noisy layer and save the reward
            R[i] = self.fn(es.forward)

        # normalize the rewards
        A = (R - np.mean(R)) / np.std(R)

        # update layers
        for n, i in zip(N, range(len(self.layers))):
            n = np.array(n)

            # np.dot(n.T, A) scales each noise's contribution to the update by how much reward it had received
            update = self.alpha / (self.noisep * self.sigma) * np.dot(n.T, A).T
            self.layers[i] = self.layers[i] + update
            

