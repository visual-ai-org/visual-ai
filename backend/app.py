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
# In-memory dataset storage
training_data = {'features': [], 'target': []}


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/insert', methods=['POST'])
def insert_data():
    content = request.json
    features = content['features']
    target = content['target']

    training_data['features'].append(features)
    training_data['target'].append(target)

    return jsonify({"status": "success", "message": "Data inserted successfully!"})


@socketio.on('train')
def handle_train(content):
    model = content.get('model')
    epochs = content.get('epochs')
    learning_rate = content.get('learning_rate')
    output_size = content.get('output_size')
    inputs = np.array(training_data['features'])
    targets = np.array(training_data['target'])

    def update_callback(iteration, data):
        update_queue.put({'iteration': iteration, 'data': data})

    if model == 'rnn':
        input_size = content.get('input_size')
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
        input_size = content.get('input_size')

        nn = NN(input_size, output_size, learning_rate, update_callback)
        nn.train(inputs, targets, epochs)

    emit('train_complete', {'message': 'Training complete!'})


def process_updates():
    while True:
        if not update_queue.empty():
            update_data = update_queue.get()
            print(f'Emitting weights: {update_data}')  # Debug statement
            socketio.emit('epoch_update', update_data)
        time.sleep(0.02)  # Sleep for 1 second


# Start the background task using SocketIO's start_background_task
socketio.start_background_task(target=process_updates)

if __name__ == "__main__":
    socketio.run(app, debug=True)
