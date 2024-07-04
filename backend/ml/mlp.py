# Multi-Layer Perceptron Class
import json

import numpy as np

from .layer import Layer


class MLP:
    def __init__(self):
        self.layers = []

    def add_layer(self, num_perceptrons, input_size=None):
        if self.layers:
            input_size = len(self.layers[-1].perceptrons)
        print("input size", input_size)
        self.layers.append(Layer(num_perceptrons, input_size))

    def forward(self, inputs):
        # print("inputs", inputs)
        # reshape input to 3d

        activations = [inputs]
        print("inputs reshaped", activations)
        for layer in self.layers:
            inputs = layer.forward(inputs)
            activations.append(inputs)
        return activations

    def backward(self, activations, label, learning_rate):
        print("activations", activations)
        errors = label - activations[-1]
        for i in range(len(self.layers) - 1, -1, -1):
            self.layers[i].backward(errors, activations[i], learning_rate)
        return np.mean(np.square(label - activations[-1]))

    def get_model_weights(self):
        weights = []
        for i, layer in enumerate(self.layers):
            layer_weights = layer.get_weights()
            # Convert numpy arrays to lists
            serializable_layer_weights = [(w.tolist(), b.tolist()) for w, b in layer_weights]
            weights.append({
                "layer": i + 1,
                "perceptrons": serializable_layer_weights
            })
        return weights

    def get_model_weights_json(self):
        print(self.get_model_weights())
        return json.dumps(self.get_model_weights(), indent=4)

    def remove_layer(self):
        self.layers.pop()