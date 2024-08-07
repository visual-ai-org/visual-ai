import unittest
import json
from app import app, socketio
import eventlet


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.socketio = socketio.test_client(app)

    # def test_create_perceptron(self):
    #     url = '/api/create_perceptron'
    #     payload = {
    #         "identifier": "perceptron1",
    #         "input_size": 2,
    #         "learning_rate": 0.01,
    #         "epochs": 1000
    #     }
    #     response = self.app.post(url, data=json.dumps(payload), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)
    #     self.assertEqual(len(response.json), 3)  # 2 input size + 1 bias
    #
    # def test_train_perceptron(self):
    #     create_url = '/api/create_perceptron'
    #     create_payload = {
    #         "identifier": "perceptron1",
    #         "input_size": 2,
    #         "learning_rate": 0.01,
    #         "epochs": 1000
    #     }
    #     self.app.post(create_url, data=json.dumps(create_payload), content_type='application/json')
    #
    #     train_url = '/api/train_perceptron'
    #     train_payload = {
    #         "identifier": "perceptron1",
    #         "training_data": [[0, 0], [0, 1], [1, 0], [1, 1]],
    #         "labels": [0, 0, 0, 1],
    #         "logistic": False
    #     }
    #     response = self.app.post(train_url, data=json.dumps(train_payload), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json, list)
    #     self.assertEqual(len(response.json), 3)  # 2 input size + 1 bias

    def test_logistic_regression(self):
        set_input_size_url = 'api/set_input_size'
        set_input_size_payload = {
            "size": 3
        }
        self.app.post(set_input_size_url, data=json.dumps(set_input_size_payload), content_type='application/json')
        create_url = '/api/add_layer'
        create_payloads = [
            {"size": 2, "function": "sigmoid"},
            {"size": 4, "function": "sigmoid"},
            {"size": 1, "function": "sigmoid"}
        ]
        for payload in create_payloads:
            self.app.post(create_url, data=json.dumps(payload), content_type='application/json')

        set_data = '/api/set_train_data'
        data_payload = {
            "X_train": [[0, 0, 1],
                        [0, 1, 1],
                        [1, 0, 1],
                        [1, 1, 0]],
            "y_train": [[0],
                        [1],
                        [1],
                        [0]],
        }
        self.app.post(set_data, data=json.dumps(data_payload), content_type='application/json')

        # Test logistic regression with SocketIO
        logistic_payload = {
            "learning_rate": 0.02,
            "epochs": 100,
        }
        self.socketio.emit('train', logistic_payload)

        # Wait to ensure all messages are received
        eventlet.sleep(1)

        received = self.socketio.get_received()
        weight_updates = [msg['args'][0]['data'] for msg in received if msg['name'] == 'weight_update']

        self.assertGreater(len(weight_updates), 0)  # Ensure we received updates
        # assert training complete is received
        self.assertTrue(any(msg['name'] == 'training_complete' for msg in received))

if __name__ == '__main__':
    unittest.main()