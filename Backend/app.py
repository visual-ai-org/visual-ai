from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from ml.ml import create_and_return_perceptron, train_perceptron, logistic_regression
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/api/create_perceptron', methods=['POST'])
def create_perceptron():
    data = request.json
    identifier = data.get('identifier')
    input_size = data.get('input_size', 2)
    learning_rate = data.get('learning_rate', 0.01)
    epochs = data.get('epochs', 1000)
    weights = create_and_return_perceptron(identifier, input_size, learning_rate, epochs)
    return jsonify(weights)


@app.route('/api/train_perceptron', methods=['POST'])
def train_perceptron_endpoint():
    data = request.json
    identifier = data.get('identifier')
    training_data = np.array(data.get('training_data'))
    labels = np.array(data.get('labels'))
    logistic = data.get('logistic', False)
    weights = train_perceptron(identifier, training_data, labels, logistic)
    return jsonify(weights)


@socketio.on('logistic_regression')
def handle_logistic_regression(data):
    identifier = data.get('identifier')
    training_data = np.array(data.get('training_data'))
    labels = np.array(data.get('labels'))

    def update_callback(weights):
        emit('weight_update', {'weights': weights}, broadcast=True)
        print('Weights:', weights)

    weights = logistic_regression(identifier, training_data, labels, update_callback)
    emit('training_complete', {'weights': weights})


if __name__ == "__main__":
    socketio.run(app, debug=True)
