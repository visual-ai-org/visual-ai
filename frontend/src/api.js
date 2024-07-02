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
        console.error('Error:', error.message);
        throw new Error(error.message);
    }
}

async function addLayer (num_perceptrons, input_size) {
    const url = `${baseUrl}/api/add_layer`;
    try {
        const response = await axios.post(url, {
            num_perceptrons,
            input_size: 2,
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
        throw new Error(error.message);
    }
}

async function remove_layer () {
    const url = `${baseUrl}/api/remove_layer`;
    try {
        const response = await axios.delete(url, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
        throw new Error(error.message);
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
        console.error('Error:', error.message);
        throw new Error(error.message);
    }

}

const ApiComponent = () => {
    const [weights, setWeights] = useState([]);
    const [finalWeights, setFinalWeights] = useState(null);

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

        socket.on('training_complete', (data) => {
            console.log('Training complete! Final weights:', data.weights);
            setFinalWeights([data]);
        });

        socket.emit('logistic_regression', {
            learning_rate: 0.1,
            epochs: 100,
        });

        return () => {
            socket.disconnect();
            console.log('Disconnected from server');
        };

    };

    return (
        <div>
            <h1>API Interaction Example</h1>
            <button
                onClick={() => test()}>
                Test
            </button>
            <button
                onClick={() => addLayer(2, 3)}>
                Add Layer
            </button>
            <button
                onClick={() => remove_layer()}>
                Remove Layer
            </button>
            <button
                onClick={() => setTrainData([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1])}>
                Set Training Data
            </button>
            <button onClick={handleLogisticRegression}>
                Start Logistic Regression with Real-Time Updates
            </button>
            <div>
                <h2>Weights Updates</h2>
                <pre>{JSON.stringify(weights, null, 2)}</pre>
                {finalWeights && (
                    <div>
                        <h2>Final Weights</h2>
                        <pre>{JSON.stringify(finalWeights, null, 2)}</pre>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ApiComponent;