import numpy as np

class Perceptron:
    def __init__(self, input_size, learning_rate=0.01, epochs=1000):
        self.weights = np.zeros(input_size + 1)
        self.learning_rate = learning_rate
        self.epochs = epochs

    def predict(self, x):
        x = np.insert(x, 0, 1)
        activation = np.dot(self.weights, x)
        return 1 if activation >= 0 else 0

    def train(self, training_data, labels):
        for _ in range(self.epochs):
            for x, y in zip(training_data, labels):
                prediction = self.predict(x)
                self.weights += self.learning_rate * (y - prediction) * np.insert(x, 0, 1)

    def get_weights(self):
        return self.weights.tolist()

# Singleton instance of the Perceptron
perceptron_instance = None

def create_perceptron(input_size, learning_rate=0.01, epochs=1000):
    global perceptron_instance
    perceptron_instance = Perceptron(input_size, learning_rate, epochs)
    return perceptron_instance

def get_perceptron():
    global perceptron_instance
    return perceptron_instance