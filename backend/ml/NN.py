import numpy as np


class NN:
    def __init__(self, input_size, output_size, learning_rate=0.01, update_callback=None):
        self.input_size = input_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.update_callback = update_callback

        # Initialize weights and biases for a simple feedforward NN
        self.weights = np.random.randn(output_size, input_size) * 0.01
        self.biases = np.zeros((output_size, 1))

    def forward(self, inputs):
        self.last_input = inputs.reshape(-1, 1)
        self.last_output = np.dot(self.weights, self.last_input) + self.biases
        return self.last_output

    def backward(self, d_output):
        d_weights = np.dot(d_output, self.last_input.T)
        d_biases = d_output

        # Update weights and biases
        self.weights -= self.learning_rate * d_weights
        self.biases -= self.learning_rate * d_biases

    def train(self, inputs, targets, epochs):
        for epoch in range(epochs):
            loss = 0
            for x, y in zip(inputs, targets):
                output = self.forward(x)
                loss += np.sum((output - y.reshape(-1, 1)) ** 2) / 2
                d_output = output - y.reshape(-1, 1)
                self.backward(d_output)

                if self.update_callback:
                    self.update_callback(epoch, self.get_weights(epoch))

            print(f"Epoch {epoch + 1}, Loss: {loss}")

    def get_weights(self, iteration=0):
        # return in json format
        return {
            "weights": self.weights.tolist(),
            "biases": self.biases.tolist()
        }
