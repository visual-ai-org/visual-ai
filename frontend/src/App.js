import logo from "./logo.svg";
import "./App.css";
import ControlPanel from "./ControlPanel";
import { useEffect, useState } from "react";
import useLocalStorageItems from "./hooks/useLocalStorageItems";

function App() {
  const items = useLocalStorageItems(); // get the data of layers and perceptrons from local storage

  return (
    <div>
      {items != null
        ? items.map((item) => (
            <li>
              <strong> {`Layer ${item.layer}`}</strong> {item.perceptrons}{" "}
              perceptrons
            </li>
          ))
        : "No layers"}
      <ControlPanel />
    </div>
  );
}

export default App;
