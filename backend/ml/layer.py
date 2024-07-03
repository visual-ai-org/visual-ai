# Layer Class
import numpy as np

from .perceptron import Perceptron


class Layer:
    def __init__(self, num_perceptrons, input_size):
        self.perceptrons = [Perceptron(input_size) for _ in range(num_perceptrons)]

    def forward(self, inputs):
        return np.array([perceptron.predict(inputs) for perceptron in self.perceptrons])

    def backward(self, errors, previous_activations, learning_rate):
        print("errors:", errors, errors.shape)
        print("prev activations:", previous_activations, previous_activations.shape)
        deltas = (errors @ previous_activations.T) @ (1 - previous_activations)  # Sigmoid derivative
        # print("deltas", deltas)
        # print(len(self.perceptrons))
        for i, perceptron in enumerate(self.perceptrons):
            perceptron.update(previous_activations, deltas[i % len(deltas)], learning_rate)

    def get_weights(self):
        return [perceptron.get_weights() for perceptron in self.perceptrons]