# Logistic Regression for Training
class LogisticRegression:
    def __init__(self, learning_rate=0.01, epochs=1000, update_callback=None):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.update_callback = update_callback

    def train(self, mlp, X_train, y_train):
        for epoch in range(self.epochs):
            for inputs, label in zip(X_train, y_train):
                output = mlp.forward(inputs)
                error = label - output
                self._update_weights(mlp, inputs, error)

    def _update_weights(self, mlp, inputs, error):
        for layer in mlp.layers:
            for perceptron in layer.perceptrons:
                perceptron.weights += self.learning_rate * error * inputs
                perceptron.bias += self.learning_rate * error
                if self.update_callback:
                    self.update_callback(mlp.get_model_weights())