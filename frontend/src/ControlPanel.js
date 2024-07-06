import {
  DialogContent,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import PropTypes from "prop-types";
import Drawer from "@mui/material/Drawer";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import { useEffect, useState } from "react";
import Perceptron from "./Perceptron";
import Layer from "./Layer";

const drawerWidth = 400;
const layerLimit = 6;

export default function ControlPanel() {
  const [layers, setLayers] = useState(0);

  useEffect(() => {
    const layersObj = JSON.parse(localStorage.getItem("layers"));
    setLayers(Object.keys(layersObj).length);
  }, []);

  const addLayerToStorage = (layerNum) => {
    const layerInfoStr = localStorage.getItem("layers");
    const layerInfoObj = JSON.parse(layerInfoStr);
    layerInfoObj[layerNum] = 1;
    localStorage.setItem("layers", JSON.stringify(layerInfoObj));
  };

  const removeLayerFromStorage = (layerNum) => {
    const layerInfoStr = localStorage.getItem("layers");
    const layerInfoObj = JSON.parse(layerInfoStr);
    delete layerInfoObj[layerNum];
    localStorage.setItem("layers", JSON.stringify(layerInfoObj));
  };

  const handleAddClick = () => {
    if (layers < layerLimit) {
      addLayerToStorage(layers + 1);
      window.dispatchEvent(new Event("storage"));
      setLayers(layers + 1);
    }
    console.log(`number of layers is ${layers}`);
  };

  const handleRemoveClick = () => {
    if (layers > 1) {
      removeLayerFromStorage(layers);
      window.dispatchEvent(new Event("storage"));
      setLayers(layers - 1);
    }
    console.log(`number of layers is ${layers}`);
  };

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
      variant="permanent"
      anchor="right"
    >
      <DialogContent>
        <Toolbar variant="regular">
          <Typography variant="h7" color="inherit" component="div">
            Configure layers and perceptrons
          </Typography>
        </Toolbar>
        <Divider />
        <List>
          {Array.from({ length: layers }, (_, index) => (
            <Layer index={index}> </Layer>
          ))}
        </List>
      </DialogContent>
      <List
        style={{ position: "absolute", bottom: "0" }}
        component={Stack}
        direction={"row"}
        spacing={"130px"}
        sx={{ padding: "50px" }}
      >
        <ListItemButton onClick={handleAddClick}>
          <ListItemIcon>
            <AddIcon fontSize="large" />
          </ListItemIcon>
        </ListItemButton>
        <ListItemButton onClick={handleRemoveClick}>
          <RemoveIcon fontSize="large" />
        </ListItemButton>
      </List>
    </Drawer>
  );
}
