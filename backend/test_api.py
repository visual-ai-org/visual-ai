import unittest
import json
from app import app, socketio
import eventlet


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.socketio = socketio.test_client(app)

    def test_create_perceptron(self):
        url = '/api/create_perceptron'
        payload = {
            "identifier": "perceptron1",
            "input_size": 2,
            "learning_rate": 0.01,
            "epochs": 1000
        }
        response = self.app.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 3)  # 2 input size + 1 bias

    def test_train_perceptron(self):
        create_url = '/api/create_perceptron'
        create_payload = {
            "identifier": "perceptron1",
            "input_size": 2,
            "learning_rate": 0.01,
            "epochs": 1000
        }
        self.app.post(create_url, data=json.dumps(create_payload), content_type='application/json')

        train_url = '/api/train_perceptron'
        train_payload = {
            "identifier": "perceptron1",
            "training_data": [[0, 0], [0, 1], [1, 0], [1, 1]],
            "labels": [0, 0, 0, 1],
            "logistic": False
        }
        response = self.app.post(train_url, data=json.dumps(train_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 3)  # 2 input size + 1 bias

    def test_logistic_regression(self):
        # Ensure perceptron is created
        create_url = '/api/create_perceptron'
        create_payload = {
            "identifier": "perceptron1",
            "input_size": 2,
            "learning_rate": 0.01,
            "epochs": 1000
        }
        self.app.post(create_url, data=json.dumps(create_payload), content_type='application/json')

        # Test logistic regression with SocketIO
        logistic_payload = {
            "identifier": "perceptron1",
            "training_data": [[0, 0], [0, 1], [1, 0], [1, 1]],
            "labels": [0, 0, 0, 1]
        }
        self.socketio.emit('logistic_regression', logistic_payload)

        # Wait to ensure all messages are received
        eventlet.sleep(1)

        received = self.socketio.get_received()
        weight_updates = [msg['args'][0]['weights'] for msg in received if msg['name'] == 'weight_update']
        training_complete = [msg['args'][0]['weights'] for msg in received if msg['name'] == 'training_complete']

        self.assertGreater(len(weight_updates), 0)  # Ensure we received updates
        self.assertIsInstance(training_complete[0], list)  # Check final weights format

if __name__ == '__main__':
    unittest.main()