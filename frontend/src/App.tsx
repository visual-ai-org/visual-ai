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

import "reactflow/dist/style.css";
import Network from './Network';

const App: React.FC = () => {
  const [open, setOpen] = useState(false);

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
    console.log(items)
  })

  return (
    <ThemeProvider theme={theme}>
      <div style={{ flex: 1, width: '100vw', height: '100vw' }}>
        <IntroModal open={open} handleClose={handleClose} />
        <ApiComponent />
        <ParentSize>{({ width, height }) => <Network width={width} height={height} layerPerceptronMap={items}/>}</ParentSize>
        <ControlPanel />
      </div>
    </ThemeProvider>
  );
}

export default App;
