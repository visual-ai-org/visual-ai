import numpy as np

from backend.ml.NN import NN


class RNN(NN):
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01, update_callback=None):
        super().__init__(input_size, output_size, learning_rate, update_callback)
        self.hidden_size = hidden_size

        # Initialize RNN-specific weights and biases
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.01  # input to hidden
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01  # hidden to hidden
        self.Why = np.random.randn(output_size, hidden_size) * 0.01  # hidden to output
        self.bh = np.zeros((hidden_size, 1))  # hidden bias
        self.by = np.zeros((output_size, 1))  # output bias

    def forward(self, inputs):
        h_prev = np.zeros((self.hidden_size, 1))
        self.last_inputs = inputs
        self.last_hs = {0: h_prev}

        for t, x in enumerate(inputs):
            x = x.reshape(-1, 1)
            h_prev = np.tanh(np.dot(self.Wxh, x) + np.dot(self.Whh, h_prev) + self.bh)
            self.last_hs[t + 1] = h_prev

        y = np.dot(self.Why, h_prev) + self.by
        return y, h_prev

    def backward(self, d_y, y, h):
        n = len(self.last_inputs)
        d_Why = np.dot(d_y, h.T)
        d_by = d_y

        d_h = np.dot(self.Why.T, d_y)

        for t in reversed(range(n)):
            temp_h = self.last_hs[t+1]
            d_h = d_h * (1 - temp_h ** 2)

            d_bh = d_h
            d_Wxh = np.dot(d_h, self.last_inputs[t].reshape(1, -1))
            d_Whh = np.dot(d_h, self.last_hs[t].T)

            d_h = np.dot(self.Whh.T, d_h)

            # Update weights and biases
            self.Wxh -= self.learning_rate * d_Wxh
            self.Whh -= self.learning_rate * d_Whh
            self.bh -= self.learning_rate * d_bh
            self.Why -= self.learning_rate * d_Why
            self.by -= self.learning_rate * d_by

    def get_weights(self, iteration=0):
        # in json format
        return {
            'Wxh': self.Wxh.tolist(),
            'Whh': self.Whh.tolist(),
            'Why': self.Why.tolist(),
            'bh': self.bh.tolist(),
            'by': self.by.tolist(),
        }