import numpy as np

from .layer import Layer
from .mlp import Mlp


class Train:
    def __init__(self, mlp: Mlp, update_callback):
        self.mlp = mlp
        self.update_callback = update_callback

    def train(self, X_train, y_train, epochs):
        for epoch in range(epochs):
            for x, y in zip(X_train, y_train):
                self._train_single(x, y)
            if self.update_callback:
                data = {
                    "type": "loss",
                    "epoch": epoch,
                    "max_epoch": epochs,
                    "loss": self.mlp.get_loss(X_train, y_train)
                }
                self.update_callback(data)

    def _train_single(self, inp, targets):
        targets = np.array(targets).flatten()
        outputs = self.mlp.feed_forward(inp)

        errors = [targets - outputs[-1]]
        for i in range(len(self.mlp.layers) - 1, 0, -1):
            weights = np.array([p.weights for p in self.mlp.layers[i].perceptrons])
            errors.insert(0, np.dot(weights.T, errors[0]))

        for i in range(len(self.mlp.layers)):
            layer = self.mlp.layers[-1-i]
            output = outputs[-1-i]
            prev_output = outputs[-2-i]
            gradient = np.multiply(errors[-1-i], Layer.derivative(output, layer.perceptrons[0].function))
            for j, p in enumerate(layer.perceptrons):
                delta_w = self.mlp.learning_rate * gradient[j] * prev_output
                delta_b = self.mlp.learning_rate * gradient[j]
                p.update_weights(delta_w, delta_b)
                if self.update_callback:
                    data = {
                        "type": "weights",
                        "weights": self.mlp.get_model_weights_json()
                    }
                    self.update_callback(data)

