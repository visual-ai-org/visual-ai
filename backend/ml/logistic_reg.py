# Logistic Regression for Training
import numpy as np


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
            next_inputs = []
            for perceptron in layer.perceptrons:
                print(f'Perceptron weights: {perceptron.weights}')  # Debug statement
                print((self.learning_rate * error * inputs).flatten())
                print(perceptron.bias)
                print((self.learning_rate * error).flatten())
                perceptron.weights += (self.learning_rate * error * inputs).flatten()  # Broadcasting works correctly here
                perceptron.bias += (self.learning_rate * error).flatten()
                next_inputs.append(perceptron.predict(inputs))

                if self.update_callback:
                    self.update_callback(mlp.get_model_weights())
            inputs = np.array(next_inputs)