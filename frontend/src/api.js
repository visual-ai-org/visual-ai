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

const ApiComponent = () => {
    const [trainingMessage, setTrainingMessage] = useState('');
    const [trainingUpdates, setTrainingUpdates] = useState([]);
    const [features, setFeatures] = useState('0,0,0,0,0,0,0');
    const [target, setTarget] = useState();
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const featuresArray = features.split(',').map(Number);

        try {
            const response = await axios.post('http://127.0.0.1:5000/insert', {
                features: featuresArray,
                target: Number(target)
            });
            setMessage(response.data.message);
        } catch (error) {
            console.error(error);
            setMessage('Error inserting data.');
        }
    };

    const handleTrain = () => {
        setTrainingUpdates([]);
        const socket = socket_io("localhost:5000/", {
            transports: ["websocket"],
            cors: {
                origin: "http://localhost:3000/",
            },
        });

        socket.on('connect', () => {
            console.log('Connected to server');

            socket.emit('train', {
                model: 'nn',
                epochs: 5,
                learning_rate: 0.01,
                // input_size: 5,
                // output_size: 1,
            });
        });

        socket.on('train_update', (data) => {
            console.log('train_update:', data);
            setTrainingUpdates([data]);
        });

        socket.on('training_complete', (data) => {
            console.log('Training complete! Final: ', data);
            setTrainingMessage(data.message);
            socket.disconnect();
        });

        socket.on('error', (error) => {
            console.error('Error:', error.message);
        });
    };

    return (
        <div>
            <h1>Insert Data</h1>
            <button
                onClick={() => test()}>
                Test
            </button>
            <form onSubmit={handleSubmit}>
                <label>
                    Features (comma-separated):
                    <input
                        type="text"
                        value={features}
                        onChange={(e) => setFeatures(e.target.value)}
                    />
                </label>
                <br/>
                <label>
                    Target:
                    <input
                        type="text"
                        value={target}
                        onChange={(e) => setTarget(e.target.value)}
                    />
                </label>
                <br/>
                <button type="submit">Submit</button>
            </form>
            {message && <p>{message}</p>}
            <h1>Train Model</h1>
            <button onClick={handleTrain}>Start Training</button>
            {trainingMessage && <p>{trainingMessage}</p>}
            <h2>Training Updates</h2>
            <ul>
                {trainingUpdates.map((update, index) => (
                    <li key={index}>
                        Epoch {update.iteration + 1}:
                        <ul>
                            <li>Weights: {update.data.weights[0].join(', ')}</li>
                            <li>Biases: {update.data.biases[0].join(', ')}</li>
                        </ul>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ApiComponent;