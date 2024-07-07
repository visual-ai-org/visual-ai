import {
  Button, Dialog, DialogActions,
  DialogContent, DialogContentText, DialogTitle,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack, TextField,
  Toolbar,
  Typography,
} from "@mui/material";
import Drawer from "@mui/material/Drawer";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import { useEffect, useState } from "react";
import Perceptron from "./Perceptron";
import Layer from "./Layer";
import {setTrainData} from "./api";
import epoch from "./epoch";

const drawerWidth = 400;
const layerLimit = 6;

export default function ControlPanel({handleTraining, setIsTraining, training, learningRate, epochs, setLearningRate, setEpochs}) {
  const [layers, setLayers] = useState(0);
  const [open, setOpen] = useState(false);
  const [trainData, setTrainDataInput] = useState('[[0, 0], [0, 1], [1, 0], [1, 1]]');
  const [labels, setLabelsInput] = useState('[[0], [1], [1], [0]]');


  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = () => {
    // Convert the input strings to arrays and numbers
    const parsedTrainData = JSON.parse(trainData);
    const parsedLabels = JSON.parse(labels);

    setTrainData(parsedTrainData, parsedLabels);
    setIsTraining(true);
    console.log("backend shouldn't update", training);
    handleClose();
  };

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
        <div>
          <Button variant="outlined" onClick={handleClickOpen}>
            Set Training Data
          </Button>
          <Dialog open={open} onClose={handleClose}>
            <DialogTitle>Set Training Data</DialogTitle>
            <DialogContent>
              <DialogContentText>
                Please enter the training data and labels in JSON format, as well as the learning rate and epochs.
              </DialogContentText>
              <TextField
                  autoFocus
                  margin="dense"
                  id="trainData"
                  label="Training Data"
                  type="text"
                  fullWidth
                  variant="standard"
                  value={trainData}
                  onChange={(e) => setTrainDataInput(e.target.value)}
              />
              <TextField
                  margin="dense"
                  id="labels"
                  label="Labels"
                  type="text"
                  fullWidth
                  variant="standard"
                  value={labels}
                  onChange={(e) => setLabelsInput(e.target.value)}
              />
              <TextField
                  margin="dense"
                  id="learningRate"
                  label="Learning Rate"
                  type="number"
                  fullWidth
                  variant="standard"
                  value={learningRate}
                  onChange={(e) => setLearningRate(e.target.value)}
              />
              <TextField
                  margin="dense"
                  id="epochs"
                  label="Epochs"
                  type="number"
                  fullWidth
                  variant="standard"
                  value={epochs}
                  onChange={(e) => setEpochs(e.target.value)}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose}>Cancel</Button>
              <Button onClick={handleSubmit}>Submit</Button>
            </DialogActions>
          </Dialog>
        </div>
        <DialogContent>
          <Toolbar variant="regular">
            <Typography variant="h7" color="inherit" component="div">
              Configure layers and perceptrons
            </Typography>
          </Toolbar>
          <Divider/>
          <List>
            {Array.from({length: layers}, (_, index) => (
                <Layer index={index} lastIndex={layers - 1}> </Layer>
            ))}
          </List>
        </DialogContent>
        <List
            style={{position: "absolute", bottom: "0"}}
            component={Stack}
            direction={"row"}
            spacing={"130px"}
            sx={{padding: "50px"}}
        >
          <ListItemButton onClick={handleAddClick}>
            <ListItemIcon>
              <AddIcon fontSize="large"/>
            </ListItemIcon>
          </ListItemButton>
          <ListItemButton onClick={handleRemoveClick}>
            <RemoveIcon fontSize="large"/>
          </ListItemButton>
        </List>
        <Button onClick={handleTraining}>
          Start Training
        </Button>
      </Drawer>
  );
}
