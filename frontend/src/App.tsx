// import logo from "./logo.svg";
import React from 'react';
import "./App.css";
import ControlPanel from "./ControlPanel";
import { useEffect, useState } from "react";
import useLocalStorageItems from "./hooks/useLocalStorageItems";
import { Box, ThemeProvider, Typography, createTheme } from "@mui/material";
import ApiComponent from "./api";
import IntroModal from "./IntroModal";
import ReactFlow from "reactflow";
import ParentSize from '@visx/responsive/lib/components/ParentSize';
import { setInputSize } from './api';

import "reactflow/dist/style.css";
import Network from './Network';
import socket_io from "socket.io-client";

const App: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [weights, setWeights] = useState([]);
  const [epoch, setEpoch] = useState([])
  const [isTraining, setIsTraining] = useState(false)
  const [learningRate, setLearningRate] = useState(0.2);
  const [epochs, setEpochs] = useState(200);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  useEffect(() => {
    handleOpen();
  }, []);

  const items = useLocalStorageItems(); // get the data of layers and perceptrons from local storage
  const theme = createTheme({
    typography: {
      fontFamily: "Roboto, sans-serif",
      fontSize: 16,
      fontWeightRegular: 400,
      fontWeightBold: 700,
      h1: {
        fontSize: "2.5rem",
        fontWeight: 700,
        lineHeight: 1.2,
      },
      h2: {
        fontSize: "2rem",
        fontWeight: 700,
        lineHeight: 1.2,
      },
      body1: {
        fontSize: "1rem",
        fontWeight: 400,
        lineHeight: 1.5,
      },
    },
  });

  useEffect(() => {
    const setInput = async () => {
      try {
        console.log(items.get("1"))
        const response = await setInputSize(items.get("1"))
        console.log(response)
      } catch (error) {
        console.error("error setting input", error)
      }
    }

    setInput()
    console.log(items)
  }, [items.get("1")])

  const handleTraining = () => {
    const socket = socket_io("localhost:5000/", {
      transports: ["websocket"],
      // @ts-ignore
      cors: {
        origin: "http://localhost:3000/",
      },
    });

    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('weight_update', (data) => {
      console.log('Weight update:', data);
      // @ts-ignore
      setWeights([data]);
    });

    socket.on('loss_update', (data) => {
      console.log('Loss update:', data)
      // @ts-ignore
      setEpoch([data])
    })

    socket.on('training_complete', (data) => {
      console.log('Training complete!');
    });

    socket.emit('train', {
      learning_rate: Number(learningRate),
      epochs: Number(epochs),
    });

    return () => {
      socket.disconnect();
      console.log('Disconnected from server');
      setIsTraining(false)
    }
  };

  return (
      <ThemeProvider theme={theme}>
        <div style={{flex: 1, width: '100vw', height: '100vw'}}>
          <IntroModal open={open} handleClose={handleClose}/>
          {/*<ApiComponent/>*/}
          <ParentSize>{({width, height}) =>
              <Network width={width}
                       height={height}
                       layerPerceptronMap={items}
                       epoch={epoch}
                       weights={weights}
                       training={isTraining}/>}</ParentSize>
          <ControlPanel handleTraining={handleTraining}
                        setIsTraining={setIsTraining}
                        training={isTraining}
                        learningRate={learningRate}
                        epoch={epoch}
                        epochs={epochs}
                        setLearningRate={setLearningRate}
                        setEpochs={setEpochs}/>
        </div>
        <div>
          <h2>Weights Updates</h2>
          <pre>{JSON.stringify(epoch, null, 2)}</pre>
          <pre>{JSON.stringify(weights, null, 2)}</pre>
        </div>
      </ThemeProvider>
  );
}

export default App;
