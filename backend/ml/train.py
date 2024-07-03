class MLPTrainer:
    def __init__(self, learning_rate=0.01, epochs=1000, update_callback=None):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.update_callback = update_callback

    def train(self, mlp, X_train, y_train):
        error_log = []
        for epoch in range(self.epochs):
            for inputs, label in zip(X_train, y_train):
                activations = mlp.forward(inputs)
                error = mlp.backward(activations, label, self.learning_rate)
                error_log.append(error)
                if self.update_callback:
                    weights = {
                        "weights": mlp.get_model_weights(),
                        "error": error_log,
                    }
                    self.update_callback(weights)