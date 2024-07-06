import React from 'react';
import { Box, Typography } from '@mui/material';

// @ts-ignore
const Epoch = ({ epoch }) => {
    if (!epoch || epoch.length === 0) {
        return null;
    }

    return (
        <Box sx={{ m: 2, mt: 2 }}>
            <Typography
                variant="h4"
                component="h2"
                gutterBottom
                style={{
                    fontFamily: 'Arial, sans-serif',
                    fontSize: '24px',
                    fontWeight: 'bold',
                    color: '#333',
                }}
            >
                Epoch: {epoch[0].data.epoch} / {epoch[0].data.max_epoch}
            </Typography>
            <Typography
                variant="h5"
                component="p"
                style={{
                    fontFamily: 'Arial, sans-serif',
                    fontSize: '20px',
                    fontWeight: 'normal',
                    color: '#666',
                }}
            >
                Loss: {epoch[0].data.loss}
            </Typography>
        </Box>
    );
};

export default Epoch;