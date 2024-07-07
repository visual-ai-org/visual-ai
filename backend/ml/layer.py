# Layer Class
import numpy as np

from .perceptron import Perceptron


class Layer:
    def __init__(self, number_of_nodes: int, row_size: int, col_size: int, function: str = "sigmoid"):
        self.col_size = col_size
        self.num_of_nodes = number_of_nodes
        self.row_size = row_size
        self.function = function
        self.perceptrons = [Perceptron(row_size, col_size, function) for _ in range(number_of_nodes)]

    @staticmethod
    def derivative(x, function):
        if function == "sigmoid":
            return x * (1 - x)
        elif function == "soft_plus":
            return Perceptron.sigmoid(x)
        elif function == "relu":
            return np.where(x > 0, 1, 0)

    def forward(self, x):
        activation_arr = np.array([])
        x = np.array(x)

        # Loop through each perceptron in self.perceptrons
        for p in self.perceptrons:
            # Apply the activate function of the perceptron to the input x
            activation_result = p.activate(x[-1])

            # Append the activation result to the list
            activation_arr = np.append(activation_arr, activation_result)

        return activation_arr

    def set_row_size(self, row_size):
        self.row_size = row_size
        self.perceptrons = [Perceptron(self.row_size, self.col_size, self.function) for _ in range(self.num_of_nodes)]

