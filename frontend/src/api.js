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

async function createPerceptron(identifier, inputSize, learningRate, epochs) {
    const url = `${baseUrl}/api/create_perceptron`;
    const payload = {
        identifier: identifier,
        input_size: inputSize,
        learning_rate: learningRate,
        epochs: epochs
    };

    try {
        const response = await axios.post(url, payload, {
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

async function trainPerceptron(identifier, trainingData, labels, logistic = false) {
    const url = `${baseUrl}/api/train_perceptron`;
    const payload = {
        identifier: identifier,
        training_data: trainingData,
        labels: labels,
        logistic: logistic
    };

    try {
        const response = await axios.post(url, payload, {
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
        throw new Error(error.message);
    }
}

// async function createLayer(identifier, numPerceptrons, inputSize, learningRate, epochs) {
//     const url = `${baseUrl}/api/create_layer`;
//     const payload = {
//         identifier: identifier,
//         numPerceptrons: numPerceptrons,
//         inputSize: inputSize,
//         learningRate: learningRate,
//         epochs: epochs
//     };
//
//     try {
//         const response = await axios.post(url, payload, {
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Access-Control-Allow-Origin': '*'
//             },
//         });
//         return response.data;
//     } catch (error) {
//         console.error('Error:', error.response?.data || error.message);
//         throw new Error(error.response?.data || error.message);
//     }
// }
//
// async function trainLayer(identifier, trainingData, labels) {
//     const url = `${baseUrl}/api/train_layer`;
//     const payload = {
//         identifier: identifier,
//         trainingData: trainingData,
//         labels: labels
//     };
//
//     try {
//         const response = await axios.post(url, payload, {
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Access-Control-Allow-Origin': '*'
//             },
//         });
//         return response.data;
//     } catch (error) {
//         console.error('Error:', error.response?.data || error.message);
//         throw new Error(error.response?.data || error.message);
//     }
// }

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
            console.log('Weight update:', data.weights);
            setWeights([data.weights]);
        });

        socket.on('training_complete', (data) => {
            console.log('Training complete! Final weights:', data.weights);
            setFinalWeights(data.weights);
        });

        socket.emit('logistic_regression', {
            identifier: 'perceptron1',
            training_data: [[0, 0], [0, 1], [1, 0], [1, 1]],
            labels: [0, 0, 0, 1]
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
                onClick={() => createPerceptron('perceptron1', 2, 0.01, 1000).then(data => console.log('Created Perceptron:', data))}>
                Create Perceptron
            </button>
            <button
                onClick={() => trainPerceptron('perceptron1', [[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1]).then(data => console.log('Trained Perceptron:', data))}>
                Train Perceptron
            </button>
            {/*<button onClick={() => createLayer('layer1', 3, 2, 0.01, 1000).then(data => console.log('Created Layer:', data))}>*/}
            {/*    Create Layer*/}
            {/*</button>*/}
            {/*<button onClick={() => trainLayer('layer1', [[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1]).then(data => console.log('Trained Layer:', data))}>*/}
            {/*    Train Layer*/}
            {/*</button>*/}
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