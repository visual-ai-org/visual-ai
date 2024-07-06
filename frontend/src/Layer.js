import React, { useState } from 'react';
import { ListItemButton, ListItemText } from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import Perceptron from './Perceptron'; // Assuming Perceptron is another component

export default function Layer({ index, lastIndex }) {
    const [isOpen, setIsOpen] = useState(false);

    const handleIsOpen = () => {
        setIsOpen((prev) => !prev);
    };

    return (
        <div>
            <ListItemButton onClick={handleIsOpen}>
                {index === 0 ? (
                    <ListItemText primary="Input Layer" sx={{ padding: '8px' }} />
                ) : index === lastIndex ? (
                    <ListItemText primary="Output Layer" sx={{ padding: '8px' }} />
                ) : (
                    <ListItemText primary={`Layer ${index}`} sx={{ padding: '8px' }} />
                )}

                {isOpen ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            <Perceptron isExpanded={isOpen} layerNumber={index + 1} />
        </div>
    );
}
