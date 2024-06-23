import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import { ListItemButton, ListItemText } from "@mui/material";
import { useState } from "react";
import Perceptron from "./Perceptron";

export default function Layer({ index }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleIsOpen = () => {
    setIsOpen((prev) => !prev);
  };

  return (
    <div>
      <ListItemButton onClick={handleIsOpen}>
        <ListItemText primary={`Layer ${index + 1}`} sx={{ padding: "8px" }} />
        {isOpen ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Perceptron isExpanded={isOpen} layerNumber={index + 1}/>
    </div>
  );
}
