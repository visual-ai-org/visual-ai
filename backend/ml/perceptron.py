import numpy as np


class Perceptron:
    def __init__(self, input_size, learning_rate=0.01, epochs=1000, update_callback=None):
        self.weights = np.zeros(input_size + 1)
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.update_callback = update_callback

    def predict(self, x):
        x = np.insert(x, 0, 1)
        activation = np.dot(self.weights, x)
        return 1 if activation >= 0 else 0

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, x):
        x = np.insert(x, 0, 1)
        activation = np.dot(self.weights, x)
        return self.sigmoid(activation)

    def train(self, training_data, labels, logistic=False):
        for _ in range(self.epochs):
            for x, y in zip(training_data, labels):
                if logistic:
                    prediction = self.predict_proba(x)
                    error = y - prediction
                    self.weights += self.learning_rate * error * np.insert(x, 0, 1)
                else:
                    prediction = self.predict(x)
                    self.weights += self.learning_rate * (y - prediction) * np.insert(x, 0, 1)
                if self.update_callback:
                    self.update_callback(self.weights.tolist())

    def get_weights(self):
        return self.weights.tolist()


# Singleton instances of Perceptrons
perceptrons = {}


def create_perceptron(identifier, input_size, learning_rate=0.01, epochs=1000, update_callback=None):
    global perceptrons
    perceptrons[identifier] = Perceptron(input_size, learning_rate, epochs, update_callback)
    return perceptrons[identifier]


def get_perceptron(identifier):
    global perceptrons
    return perceptrons.get(identifier)
