from .perceptron import create_perceptron, get_perceptron


def create_and_return_perceptron(identifier, input_size, learning_rate=0.01, epochs=1000, update_callback=None):
    perceptron = create_perceptron(identifier, input_size, learning_rate, epochs, update_callback)
    return perceptron.get_weights()


def train_perceptron(identifier, training_data, labels, logistic=False, update_callback=None):
    perceptron = get_perceptron(identifier)
    if perceptron is None:
        raise ValueError("Perceptron not created. Please create a perceptron first.")
    perceptron.update_callback = update_callback
    perceptron.train(training_data, labels, logistic)
    return perceptron.get_weights()


def logistic_regression(identifier, training_data, labels, update_callback):
    return train_perceptron(identifier, training_data, labels, logistic=True, update_callback=update_callback)
