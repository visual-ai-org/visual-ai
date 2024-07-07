# Multi-Layer Perceptron Class
import json
import operator

import numpy as np

from .layer import Layer


class Mlp:
    def __init__(self, init_nodes: int = 0, learning_rate: float = .2) -> None:
        self.layers = []
        self.learning_rate = learning_rate
        if init_nodes > 0:
            self.input_size = init_nodes

    def add_layer(self, number_of_nodes: int, function="sigmoid"):
        row_size = number_of_nodes
        if self.layers:
            col_size = self.layers[-1].row_size
        else:
            col_size = self.input_size
        self.layers.append(Layer(number_of_nodes, row_size, col_size, function))

        for layer in self.layers:
            print("nodes", layer.num_of_nodes, layer.perceptrons[0].weights.shape)
        print()


    def get_model_weights(self):
        model_weights = {}
        for i, layer in enumerate(self.layers):
            layer_weights = {}
            for j, perceptron in enumerate(layer.perceptrons):
                layer_weights[f'perceptron {j}'] = {
                    'weights': perceptron.weights.copy(),
                    'bias': perceptron.bias
                }
            model_weights[f'layer {i}'] = layer_weights
        return model_weights

    def get_model_weights_json(self):
        model_weights = {}
        for i, layer in enumerate(self.layers):
            layer_weights = {}
            for j, perceptron in enumerate(layer.perceptrons):
                layer_weights[f'perceptron {j}'] = {
                    'weights': perceptron.weights.tolist(),
                    'bias': perceptron.bias  # Convert to scalar for JSON serialization
                }
            model_weights[f'layer {i}'] = layer_weights
        return model_weights

    def get_loss(self, X, y):
        total_loss = 0
        for inp, target in zip(X, y):
            predicted = self.feed_forward(inp)[-1]
            total_loss += np.mean((target - predicted) ** 2)
        return total_loss / len(X)

    def feed_forward(self, inp):
        outputs = [np.matrix(inp).T]
        for layer in self.layers:
            outputs = layer.forward(outputs)
            print("outputs", outputs)
        return outputs

    def predict(self, inp):
        output = self.feed_forward(inp)[-1]
        output = dict(enumerate(output))
        out_class = max(output.items(), key=operator.itemgetter(1))[0]
        out_prob = output[out_class]
        return out_class, out_prob

    def remove_layer(self):
        self.layers.pop()