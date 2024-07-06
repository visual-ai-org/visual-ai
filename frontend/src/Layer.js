import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import { ListItemButton, ListItemText } from "@mui/material";
import { useState } from "react";
import Perceptron from "./Perceptron";
import { setInputSize } from "./api";

export default function Layer({ index }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleIsOpen = () => {
    setIsOpen((prev) => !prev);
  };

  return (
    <div>
      <ListItemButton onClick={handleIsOpen}>
        {index !== 0 ? (
          <ListItemText primary={`Layer ${index}`} sx={{ padding: "8px" }} />
        ) : (
          <ListItemText primary={`Input Layer`} sx={{ padding: "8px" }} />
        )}

        {isOpen ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Perceptron isExpanded={isOpen} layerNumber={index + 1} />
    </div>
  );
}
