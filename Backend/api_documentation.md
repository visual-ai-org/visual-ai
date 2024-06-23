# API Documentation

## Base URL
The base URL for all endpoints is: http://127.0.0.1:5000

## Endpoints

### 1. Create Perceptron

**Endpoint:** `/api/create_perceptron`

**Method:** `POST`

**Description:** Creates a new Perceptron instance with the specified input size, learning rate, and number of epochs.

**Request Payload:**
```json
{
    "input_size": 2,         // Number of inputs (excluding the bias)
    "learning_rate": 0.01,   // Learning rate for the Perceptron
    "epochs": 1000           // Number of training epochs
}
```
**Response:**
```json
{
  "weights": [0.0, 0.0, 0.0]  // Initial weights of the Perceptron (including the bias)
}
```
**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/create_perceptron -H "Content-Type: application/json" -d '{"input_size": 2, "learning_rate": 0.01, "epochs": 1000}'
```
**Example Response:**
```json
{
  "weights": [0.0, 0.0, 0.0]
}
```
### 2. Train Perceptron
**Endpoint:** `/api/train_perceptron`

**Method:** `POST`

**Description:** Trains the Perceptron instance with the provided training data and labels, and returns the updated weights.

**Request Payload:**
```json
{
  "training_data": [[0, 0], [0, 1], [1, 0], [1, 1]],  // Training data (input features)
  "labels": [0, 0, 0, 1]                             // Corresponding labels (output)
}
```
**Response:**
```json
{
  "weights": [0.01, 0.01, 0.01]  // Updated weights of the Perceptron (including the bias)
}
```
**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/train_perceptron -H "Content-Type: application/json" -d '{"training_data": [[0, 0], [0, 1], [1, 0], [1, 1]], "labels": [0, 0, 0, 1]}'
```
**Example Response:**
```json
{
  "weights": [0.02, 0.01, 0.01]
}
```

### 3. Logistic Regression
**Endpoint:** `/api/logistic_regression`

**Method:** `POST`

**Description:** 	
- Use the WebSocket event logistic_regression with the specified payload to start logistic regression training.
- The server will send real-time updates of the weights through the weight_update event and notify when training is complete with the training_complete event.


**Request Payload:**
```json
{
    "identifier": "perceptron1",  // Unique identifier for the Perceptron
    "training_data": [[0, 0], [0, 1], [1, 0], [1, 1]],  // Training data (input features)
    "labels": [0, 0, 0, 1]        // Corresponding labels (output)
}
```

**Real-Time Updates:**
- Event: weight_update
  ```json
  {
    "weights": [0.01, 0.01, 0.01]  // Current weights of the Perceptron (including the bias)
  }
  ```
- Event: training_complete
  ```json
  {
    "weights": [0.02, 0.01, 0.01]  // Final weights of the Perceptron (including the bias)
  }
  ```

**Example Frontend Integration:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Logistic Regression</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <h1>Logistic Regression Training</h1>
    <pre id="output"></pre>

    <script>
        var socket = io('http://127.0.0.1:5000');

        socket.on('connect', function() {
            console.log('Connected to server');
            socket.emit('logistic_regression', {
                identifier: 'perceptron1',
                training_data: [[0, 0], [0, 1], [1, 0], [1, 1]],
                labels: [0, 0, 0, 1]
            });
        });

        socket.on('weight_update', function(data) {
            document.getElementById('output').textContent += 'Weights: ' + data.weights + '\n';
        });

        socket.on('training_complete', function(data) {
            document.getElementById('output').textContent += 'Training complete! Final weights: ' + data.weights + '\n';
        });
    </script>
</body>
</html>
```
