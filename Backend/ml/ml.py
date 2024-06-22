from perceptron import create_perceptron, get_perceptron


def create_and_return_perceptron():
    perceptron = create_perceptron(input_size=2)
    return perceptron.get_weights()


def train_perceptron(training_data, labels):
    perceptron = get_perceptron()
    if perceptron is None:
        raise ValueError("Perceptron not created. Please create a perceptron first.")
    perceptron.train(training_data, labels)
    return perceptron.get_weights()
