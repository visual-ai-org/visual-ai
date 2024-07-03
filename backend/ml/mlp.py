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