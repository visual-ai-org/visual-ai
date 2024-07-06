# API Documentation

## Base URL
The base URL for all endpoints is: http://127.0.0.1:5000

## Endpoints

### 1. Add Layer

**Endpoint:** `/api/add_layer`

**Method:** `POST`

**Description:** Adds a new layer to the Perceptron instance with the specified number of perceptrons and activation function. The weights are initialized randomly and can be trained using the train_perceptron endpoint. The Perceptron can be trained using the logistic_regression endpoint to perform logistic regression on the training data.

**Request Payload:**
```json
{
    "size": 2,         // Number of perceptrons in the layer
    "function": "sigmoid",   // Activation function (sigmoid, relu, tanh)
}
```
**Response:**
```json
{
  "message": "Layer added successfully",
  "weights": Object // json object representing the layers weights
}
```
**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/add_layer -H "Content-Type: application/json" -d '{"size": 2, "function": "sigmoid"}'
```
### 2. Set Input Size
**Endpoint:** `/api/set_input_size`

**Method:** `POST`

**Description:** Sets the input size for the Neural Network.

**Request Payload:**
```json
{
    "size": 2  // input size (no. of columns/features)
}
```
**Response:**
```json
{
  "message": "Input size set successfully"  
}
```
**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/set_input_size -H "Content-Type: application/json" -d '{"size": 2}'
```

### 3. Remove Layer
**Endpoint:** `/api/remove_layer`

**Method:** `DELETE`

**Description:** Removes the last layer from the Neural Network.

**Response:**
```json
{
  "message": "Layer removed successfully",
  "weights": Object // json object representing the layers weights
}
```

**Example Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/remove_layer
```

### 4. Set Train Data
**Endpoint:** `/api/set_train_data`

**Method:** `POST`

**Description:** Sets the training data and labels for the Neural Network.

**Request Payload:**
```json
{
    X_train: [[0, 0], [0, 1], [1, 0], [1, 1]],  // Training data
    y_train: [[0], [1], [1], [0]]  // Labels
}
```

**Response:**
```json
{
  "message": "{X_train}, {y_train}"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/set_train_data -H "Content-Type: application/json" -d '{"X_train": [[0, 0], [0, 1], [1, 0], [1, 1]], "y_train": [[0], [1], [1], [0]]}'
```

### 4. Train
**Endpoint:** `train`

**Method:** `SOCKET`

**Description:** 	
- Trains the Neural Network using the specified training data and labels.
- The training data and labels are sent to the server using the 'train' event.
- The server will send real-time updates to the client using the 'weight_update' event.
- The server will send 'loss_update' event to update the loss value.
- Once the training is complete, the server will send the 'training_complete' event.

**Request Payload:**
```json
{
    learning_rate: 0.01,  // Learning rate for the training (optional, default: 0.01)
    epochs: 1000          // Number of epochs to train the Neural Network (optional, default: 1000)
}
```

**Real-Time Updates:**
1. Event: weight_update
  ```json
  {
    "data": Object  // Current weights of the Neural Network
  }
  ```

2. Event: loss_update
  ```json
  {
    "data": Object  // Current loss value of the Neural Network
  }
  ```
  
3. Event: training_complete