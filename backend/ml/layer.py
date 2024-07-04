# Layer Class
import numpy as np

from .perceptron import Perceptron


class Layer:
    def __init__(self, num_perceptrons, input_size):
        self.perceptrons = [Perceptron(input_size) for _ in range(num_perceptrons)]

    def forward(self, inputs):
        return np.array([perceptron.predict(inputs) for perceptron in self.perceptrons])

    def backward(self, errors, previous_activations, learning_rate):
        print("prev activations:", previous_activations.shape)
        print("errors:", errors.shape)
        print("previous_activations @ errors", (previous_activations @ errors).shape)
        print("1 - previous_activations", (1 - previous_activations).shape)

        deltas = previous_activations @ errors @ (1 - previous_activations).T  # Sigmoid derivative
        # print("deltas", deltas)
        # print(len(self.perceptrons))
        for i, perceptron in enumerate(self.perceptrons):
            perceptron.update(previous_activations, deltas[i % len(deltas)], learning_rate)

    def get_weights(self):
        return [perceptron.get_weights() for perceptron in self.perceptrons]