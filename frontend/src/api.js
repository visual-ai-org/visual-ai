import React, { useState, useEffect } from 'react';
import axios from 'axios';
import socket_io from 'socket.io-client';

const baseUrl = 'http://localhost:5000';

async function test() {
    const url = `${baseUrl}`;
    try {
        const response = await axios.get(url, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        throw new Error(error.response ? error.response.data : error.message);
    }
}

async function setInputSize (size) {
    const url = `${baseUrl}/api/set_input_size`;
    try {
        const response = await axios.post(url, {
            size: size,
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        throw new Error(error.response ? error.response.data : error.message);
    }
}

async function addLayer (num_perceptrons, func) {
    const url = `${baseUrl}/api/add_layer`;
    try {
        const response = await axios.post(url, {
            size: num_perceptrons,
            function: func,
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        throw new Error(error.response ? error.response.data : error.message);
    }
}

async function remove_layer (index) {
    const url = `${baseUrl}/api/remove_layer`;
    try {
        const response = await axios.delete(url, {
            index: index
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        throw new Error(error.response ? error.response.data : error.message);
    }
}

async function setTrainData (train_data, labels) {
    const url = `${baseUrl}/api/set_train_data`;
    try {
        const response = await axios.post(url, {
            X_train: train_data,
            y_train: labels,
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        throw new Error(error.response ? error.response.data : error.message);
    }

}

const ApiComponent = () => {
    const [weights, setWeights] = useState([]);
    const [epoch, setEpoch] = useState([])

    useEffect(() => {

    }, []);

    const handleLogisticRegression = () => {
        const socket = socket_io("localhost:5000/", {
            transports: ["websocket"],
            cors: {
                origin: "http://localhost:3000/",
            },
        });

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('weight_update', (data) => {
            console.log('Weight update:', data);
            setWeights([data]);
        });

        socket.on('loss_update', (data) => {
            console.log('Loss update:', data)
            setEpoch([data])
        })

        socket.on('training_complete', (data) => {
            console.log('Training complete!');
        });

        socket.emit('train', {
            learning_rate: 0.02,
            epochs: 100,
        });

        return () => {
            socket.disconnect();
            console.log('Disconnected from server');
        }
    };

    return (
        <div>
            <h1>API Interaction Example</h1>
            <button
                onClick={() => test()}>
                Test
            </button>
            <button
                onClick={() => {
                    setInputSize(2)
                    addLayer(2, "sigmoid")
                    addLayer(1, "sigmoid")
                }}>
                Add Layer
            </button>
            <button
                onClick={() => remove_layer()}>
                Remove Layer
            </button>
            <button
                onClick={() => setTrainData([[0, 0], [0, 1], [1, 0], [1, 1]], [[0], [1], [1], [0]])}>
                Set Training Data
            </button>
            <button onClick={handleLogisticRegression}>
                Start Logistic Regression with Real-Time Updates
            </button>
            <div>
                <h2>Weights Updates</h2>
                <pre>{JSON.stringify(epoch, null, 2)}</pre>
                <pre>{JSON.stringify(weights, null, 2)}</pre>
            </div>
        </div>
    );
};

export default ApiComponent;