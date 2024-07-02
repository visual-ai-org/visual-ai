import traceback

import eventlet

from backend.ml.CNN import CNN
from backend.ml.NN import NN
from backend.ml.RNN import RNN

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
# Sample training data
training_data = [
    {"features": [0.5, 0.3, 0.8, 0.1, 0.6], "target": 1.0},
    {"features": [0.9, 0.4, 0.2, 0.7, 0.3], "target": 0.0},
    {"features": [0.2, 0.1, 0.4, 0.8, 0.9], "target": 1.0},
    {"features": [0.6, 0.5, 0.7, 0.2, 0.1], "target": 0.0},
    {"features": [0.3, 0.8, 0.9, 0.5, 0.2], "target": 1.0}
]

input_size = 5
output_size = 1

@app.route('/')
def home():
    return "Hello, Flask!"


# @app.route('/insert', methods=['POST'])
# def insert_data():
    # content = request.json
    # features = content['features']
    # target = content['target']
    #
    # training_data.append({"features": features, "target": target})
    #
    # return jsonify({"status": "success", "message": "Data inserted successfully!"})


@socketio.on('train')
def handle_train(content):
    model = content.get('model')
    epochs = content.get('epochs')
    learning_rate = content.get('learning_rate')
    inputs = np.array([data['features'] for data in training_data])
    targets = np.array([data['target'] for data in training_data])
    print(f'Model: {model}, Epochs: {epochs}, Learning Rate: {learning_rate}')  # Debug statement

    def update_callback(iteration, data):
        update_queue.put({'iteration': iteration, 'data': data})

    try:
        if model == 'rnn':
            hidden_size = content.get('hidden_size')

            rnn = RNN(input_size, hidden_size, output_size, learning_rate, update_callback)
            rnn.train(inputs, targets, epochs)
        elif model == 'cnn':
            input_shape = content.get('input_shape')
            num_filters = content.get('num_filters')
            filter_size = content.get('filter_size')

            cnn = CNN(input_shape, num_filters, filter_size, output_size, learning_rate, update_callback)
            cnn.train(inputs, targets, epochs)
        else:
            nn = NN(input_size, output_size, learning_rate, update_callback)
            nn.train(inputs, targets, epochs)
    except Exception as e:
        # print with traceback
        print(traceback.format_exc())
        socketio.emit('error', {'message': str(e)})
        return

    emit('train_complete', {'message': 'Training complete!'})


def process_updates():
    while True:
        if not update_queue.empty():
            update_data = update_queue.get()
            print(f'Emitting weights: {update_data}')  # Debug statement
            socketio.emit('train_update', update_data)
        time.sleep(0.02)  # Sleep for 1 second


# Start the background task using SocketIO's start_background_task
socketio.start_background_task(target=process_updates)

if __name__ == "__main__":
    socketio.run(app, debug=True)
