import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    headers = {'Content-Type': 'application/json'}

    def test_create_perceptron(self):
        url = f"{self.BASE_URL}/api/create_perceptron"
        payload = {
            "input_size": 2,
            "learning_rate": 0.01,
            "epochs": 1000
        }
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)  # 2 input size + 1 bias

    def test_train_perceptron(self):
        # First, create the perceptron
        create_url = f"{self.BASE_URL}/api/create_perceptron"
        create_payload = {
            "input_size": 2,
            "learning_rate": 0.01,
            "epochs": 1000
        }
        create_response = requests.post(create_url, data=json.dumps(create_payload), headers=self.headers)
        self.assertEqual(create_response.status_code, 200)

        # Now train the perceptron
        train_url = f"{self.BASE_URL}/api/train_perceptron"
        train_payload = {
            "training_data": [[0, 0], [0, 1], [1, 0], [1, 1]],
            "labels": [0, 0, 0, 1]
        }
        train_response = requests.post(train_url, data=json.dumps(train_payload), headers=self.headers)
        self.assertEqual(train_response.status_code, 200)
        self.assertIsInstance(train_response.json(), list)
        self.assertEqual(len(train_response.json()), 3)  # 2 input size + 1 bias

if __name__ == "__main__":
    unittest.main()