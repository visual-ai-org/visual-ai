import numpy as np
from flask import Flask, jsonify, request

from ml.ml import create_and_return_perceptron, train_perceptron

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/api/create_perceptron', methods=['POST'])
def create_perceptron():
    # Example payload: {"input_size": 2, "learning_rate": 0.01, "epochs": 1000}
    data = request.json
    input_size = data.get('input_size', 2)
    learning_rate = data.get('learning_rate', 0.01)
    epochs = data.get('epochs', 1000)
    weights = create_and_return_perceptron()
    return jsonify(weights)


@app.route('/api/train_perceptron', methods=['POST'])
def train_perceptron_endpoint():
    # Example payload: {"training_data": [[0, 0], [0, 1], [1, 0], [1, 1]], "labels": [0, 0, 0, 1]}
    data = request.json
    training_data = np.array(data.get('training_data'))
    labels = np.array(data.get('labels'))
    weights = train_perceptron(training_data, labels)
    return jsonify(weights)


if __name__ == "__main__":
    app.run(debug=True)
