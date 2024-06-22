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

## Example Workflow
### 1. Create a Perceptron:
- Send a POST request to /api/create_perceptron with the desired input size, learning rate, and number of epochs.
- Example:
    ```bash
    curl -X POST http://127.0.0.1:5000/api/create_perceptron -H "Content-Type: application/json" -d '{"input_size": 2, "learning_rate": 0.01, "epochs": 1000}'
    ```
- 	This will initialize the Perceptron with the specified parameters and return the initial weights.
### 2. Train the Perceptron:
- Send a POST request to /api/train_perceptron with the training data and labels.
- Example:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/train_perceptron -H "Content-Type: application/json" -d '{"training_data": [[0, 0], [0, 1], [1, 0], [1, 1]], "labels": [0, 0, 0, 1]}
  ```
- This will train the Perceptron with the provided data and return the updated weights.

