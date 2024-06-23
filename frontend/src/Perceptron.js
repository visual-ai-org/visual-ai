import {
  Collapse,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
} from "@mui/material";
import { useEffect, useState } from "react";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";

const perceptronLimit = 5;

export default function Perceptron({ isExpanded, layerNumber }) {
  const [perceptronNum, setPerceptronNum] = useState(0);

  useEffect(() => {
    const layersObj = JSON.parse(localStorage.getItem("layers"));
    const perceptrons = layersObj[layerNumber];
    setPerceptronNum(perceptrons);
  }, [layerNumber]);

  const addPerceptronToStorage = (layerNumber) => {
    const layerInfoStr = localStorage.getItem("layers");
    const layerInfoObj = JSON.parse(layerInfoStr);
    layerInfoObj[layerNumber] += 1;
    localStorage.setItem("layers", JSON.stringify(layerInfoObj));
  };

  const removePerceptronFromStorage = (layerNumber) => {
    const layerInfoStr = localStorage.getItem("layers");
    const layerInfoObj = JSON.parse(layerInfoStr);
    layerInfoObj[layerNumber] -= 1;
    localStorage.setItem("layers", JSON.stringify(layerInfoObj));
  };

  const handleAddClick = () => {
    if (perceptronNum < perceptronLimit) {
      addPerceptronToStorage(layerNumber);
      window.dispatchEvent(new Event("storage"));
      setPerceptronNum(perceptronNum + 1);
    }
    console.log(`number of perceptrons is ${perceptronNum}`);
  };

  const handleRemoveClick = () => {
    if (perceptronNum > 1) {
      removePerceptronFromStorage(layerNumber);
      window.dispatchEvent(new Event("storage"));
      setPerceptronNum(perceptronNum - 1);
    }
    console.log(`number of perceptrons is ${perceptronNum}`);
  };

  return (
    <Collapse in={isExpanded} timeout={"auto"} unmountOnExit>
      <List component={Stack} direction={"row"} spacing={"50px"}>
        <ListItemButton>
          <ListItemText
            primary={
              perceptronNum > 1
                ? `${perceptronNum} perceptrons`
                : `${perceptronNum} perceptron`
            }
            sx={{ paddingLeft: "16px" }}
          />
        </ListItemButton>
        <List component={Stack} direction={"row"}>
          <ListItemButton onClick={handleAddClick}>
            <ListItemIcon>
              <AddIcon fontSize="small" />
            </ListItemIcon>
          </ListItemButton>
          <ListItemButton onClick={handleRemoveClick}>
            <RemoveIcon fontSize="small" />
          </ListItemButton>
        </List>
      </List>
    </Collapse>
  );
}
