# Multi-Layer Perceptron Class
import json

from .layer import Layer


class MLP:
    def __init__(self):
        self.layers = []

    def add_layer(self, num_perceptrons, input_size=None):
        if self.layers:
            input_size = len(self.layers[-1].perceptrons)
        self.layers.append(Layer(num_perceptrons, input_size))

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def get_model_weights(self):
        weights = []
        for i, layer in enumerate(self.layers):
            layer_weights = layer.get_weights()
            weights.append({
                "layer": i + 1,
                "perceptrons": layer_weights
            })
        return weights

    def get_layers(self):
        return json.dumps([layer.__dict__ for layer in self.layers])

    def remove_layer(self):
        self.layers.pop()