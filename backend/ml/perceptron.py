import numpy as np


# Perceptron Class
class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)
        self.bias = np.random.rand(1)

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs):
        print(self.weights.shape)
        print("inputs", inputs, "weights", self.weights, "bias", self.bias)

        return self.activate(np.dot(inputs.T, self.weights) + self.bias)

    def get_weights(self):
        return self.weights, self.bias

    def update(self, inputs, delta, learning_rate):
        print("weights:", self.weights)
        print("lr:", (learning_rate * delta * inputs))
        self.weights = self.weights + (learning_rate * delta * inputs)
        print("weights new:", self.weights)

    # print("bias:", self.bias)
        # print("lr:", (learning_rate * delta).reshape(-1, 1).T)
        self.bias = self.bias @ (learning_rate * delta).reshape(-1, 1).T
        # print("new bias:", self.bias)
