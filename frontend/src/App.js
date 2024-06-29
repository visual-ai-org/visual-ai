import logo from "./logo.svg";
import "./App.css";
import ControlPanel from "./ControlPanel";
import { useEffect, useState } from "react";
import useLocalStorageItems from "./hooks/useLocalStorageItems";
import {Box} from "@mui/material";
import ApiComponent from "./api";

function App() {
  const items = useLocalStorageItems(); // get the data of layers and perceptrons from local storage

  return (
    <div>
        <Box>
            <ApiComponent/>
            {items != null
                ? items.map((item) => (
                    <li>
                  <strong> {`Layer ${item.layer}`}</strong> {item.perceptrons}{" "}
                  perceptrons
                </li>
              ))
            : "No layers"}
        </Box>
        <ControlPanel />
    </div>
  );
}

export default App;
