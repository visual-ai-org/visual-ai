import eventlet

eventlet.monkey_patch()  # This must be the very first import

from ml.mlp import Mlp
from ml import mlp
from ml.train import Train



import time
import numpy as np
from queue import Queue
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}}, origins=["http://localhost:3000"])
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

update_queue = Queue()
mlp = mlp.Mlp(init_nodes=2, learning_rate=0.2)
X_train = []
y_train = []

@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/api/add_layer', methods=['POST'])
def add_layer():
    data = request.json
    try:
        num_of_nodes = data['size']
        function = data['function']
        mlp.add_layer(num_of_nodes, function=function)
        weights = mlp.get_models_weight_json()
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Layer added successfully", "weights": weights}), 200


@app.route('/api/set_input_size', methods=['POST'])
def set_input_size():
    data = request.json
    try:
        size = data['size']
        mlp.number_of_nodes[0] = size
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Input size set successfully"}), 200


@app.route('/api/remove_layer', methods=['DELETE'])
def remove_layer():
    try:
        mlp.remove_layer()
        return jsonify({"message": "Layer removed successfully", "weights": mlp.get_models_weight_json()}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Layer is empty"}), 200


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

    mlp.learning_rate = learning_rate

    def update_callback(data):
        # print(f'Putting weights in queue: {data}')  # Debug statement
        update_queue.put(data)

    trainer = Train(mlp, update_callback)
    trainer.train(X_train, y_train, epochs)

    socketio.emit('training_complete')


def process_updates():
    while True:
        if not update_queue.empty():
            data = update_queue.get()

            if data['type'] == 'weights':
                # print(f'Emitting Weights: {data}')
                socketio.emit('weight_update', {'data': data})
            elif data['type'] == "loss":
                # print(f'Emitting Loss: {data}')
                socketio.emit('loss_update', {'data': data})
        time.sleep(0.02)  # Sleep for 1 second


# Start the background task using SocketIO's start_background_task
socketio.start_background_task(target=process_updates)

if __name__ == "__main__":
    socketio.run(app, debug=True)
