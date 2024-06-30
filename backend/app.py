import eventlet

eventlet.monkey_patch()  # This must be the very first import

import time
import numpy as np
from queue import Queue
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from ml.ml import create_and_return_perceptron, train_perceptron, logistic_regression

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

update_queue = Queue()


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
        print(f'Putting weights in queue: {weights}')  # Debug statement
        update_queue.put(weights)

    weights = logistic_regression(identifier, training_data, labels, update_callback)
    socketio.emit('training_complete', {'weights': weights})


def process_updates():
    while True:
        if not update_queue.empty():
            weights = update_queue.get()
            print(f'Emitting weights: {weights}')  # Debug statement
            socketio.emit('weight_update', {'weights': weights})
        time.sleep(0.02)  # Sleep for 1 second


# Start the background task using SocketIO's start_background_task
socketio.start_background_task(target=process_updates)

if __name__ == "__main__":
    socketio.run(app, debug=True)
