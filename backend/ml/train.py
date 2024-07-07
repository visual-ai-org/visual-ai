import numpy as np

from .layer import Layer
from .mlp import Mlp


class Train:
    def __init__(self, mlp: Mlp, update_callback):
        self.mlp = mlp
        self.update_callback = update_callback

    def train(self, X_train, y_train, epochs):
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        for epoch in range(epochs):
            for x, y in zip(X_train, y_train):
                self._train_single(x, y)
            if self.update_callback:
                data = {
                    "type": "loss",
                    "epoch": epoch+1,
                    "max_epoch": epochs,
                    "loss": self.mlp.get_loss(X_train, y_train)
                }
                self.update_callback(data)

    def _train_single(self, inp, targets):
        self.mlp.train(inp, targets)
        if self.update_callback:
            data = {
                "type": "weights",
                "weights": self.mlp.get_models_weight_json()
            }
            self.update_callback(data)

