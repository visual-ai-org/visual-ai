import json

import eventlet

from ml.train import MLPTrainer
from ml import mlp

eventlet.monkey_patch()  # This must be the very first import

import time
import numpy as np
from queue import Queue
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

update_queue = Queue()
mlp = mlp.MLP()
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([0, 1, 1, 0])


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/api/add_layer', methods=['POST'])
def add_layer():
    data = request.json
    try:
        num_perceptrons = data['num_perceptrons']
        input_size = data.get('input_size', None)
        mlp.add_layer(num_perceptrons, input_size)
        weights = mlp.get_model_weights_json()
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Layer added successfully", "weights": weights}), 200


@app.route('/api/remove_layer', methods=['DELETE'])
def remove_layer():
    mlp.remove_layer()
    return jsonify({"message": "Layer removed successfully", "weights": mlp.get_model_weights_json()}), 200


@app.route('/api/set_train_data', methods=['POST'])
def set_train_data():
    data = request.json
    # set global X_train and y_train
    global X_train, y_train
    X_train = np.array(data['X_train'])
    y_train = np.array(data['y_train'])
    return jsonify({"message": f'{X_train}, {y_train}'}), 200


@socketio.on('train')
def handle_train(data):
    learning_rate = data.get('learning_rate', 0.01)
    epochs = data.get('epochs', 1000)

    def update_callback(weights):
        print(f'Putting weights in queue: {weights}')  # Debug statement
        update_queue.put(weights)

    trainer = MLPTrainer(learning_rate, epochs, update_callback)
    trainer.train(mlp, X_train, y_train)
    weights = mlp.get_model_weights()

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
