import numpy as np

from backend.ml.NN import NN


class CNN(NN):
    def __init__(self, input_shape, num_filters, filter_size, output_size, learning_rate=0.01, update_callback=None):
        super().__init__(input_shape[0] * input_shape[1], output_size, learning_rate, update_callback)
        self.input_shape = input_shape
        self.num_filters = num_filters
        self.filter_size = filter_size

        # Initialize CNN-specific filters and fully connected layer weights
        self.filters = np.random.randn(num_filters, filter_size, filter_size) * 0.01
        self.fc_weights = np.random.randn(output_size, num_filters * (input_shape[0] - filter_size + 1) * (input_shape[1] - filter_size + 1)) * 0.01
        self.fc_biases = np.zeros((output_size, 1))

    def forward(self, inputs):
        self.last_input = inputs
        h, w = self.input_shape
        conv_output = np.zeros((h - self.filter_size + 1, w - self.filter_size + 1, self.num_filters))

        for f in range(self.num_filters):
            for i in range(h - self.filter_size + 1):
                for j in range(w - self.filter_size + 1):
                    region = inputs[i:i+self.filter_size, j:j+self.filter_size]
                    conv_output[i, j, f] = np.sum(region * self.filters[f])

        self.conv_output = conv_output.reshape(-1, 1)
        output = np.dot(self.fc_weights, self.conv_output) + self.fc_biases
        return output

    def backward(self, d_output, y):
        # Dummy backward function for simplicity
        d_fc_weights = np.dot(d_output, self.conv_output.T)
        d_fc_biases = d_output

        d_conv_output = np.dot(self.fc_weights.T, d_output)
        d_filters = np.zeros(self.filters.shape)

        h, w = self.input_shape
        for f in range(self.num_filters):
            for i in range(h - self.filter_size + 1):
                for j in range(w - self.filter_size + 1):
                    region = self.last_input[i:i+self.filter_size, j:j+self.filter_size]
                    d_filters[f] += region * d_conv_output[i * (h - self.filter_size + 1) + j]

        # Update weights and biases
        self.filters -= self.learning_rate * d_filters
        self.fc_weights -= self.learning_rate * d_fc_weights
        self.fc_biases -= self.learning_rate * d_fc_biases

    def get_weights(self, iteration=0):
        # return in json format
        return {
            "filters": self.filters.tolist(),
            "fc_weights": self.fc_weights.tolist(),
            "fc_biases": self.fc_biases.tolist()
        }