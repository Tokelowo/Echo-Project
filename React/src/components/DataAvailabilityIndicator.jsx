import React, { useState, useEffect } from 'react';
import {
  Box,
  Alert,
  Collapse,
  IconButton,
  Typography
} from '@mui/material';
import { Info, Close } from '@mui/icons-material';

const DataAvailabilityIndicator = ({ 
  visibleSections = [], 
  totalSections = 0, 
  pageName = 'page' 
}) => {
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    // Show alert if some sections are hidden due to empty data
    if (totalSections > 0 && visibleSections.length < totalSections) {
      setShowAlert(true);
    }
  }, [visibleSections.length, totalSections]);

  if (totalSections === 0 || visibleSections.length === totalSections) {
    return null;
  }

  const hiddenCount = totalSections - visibleSections.length;

  return (
    <Collapse in={showAlert}>
      <Alert
        severity="info"
        sx={{ mb: 2 }}
        action={
          <IconButton
            aria-label="close"
            color="inherit"
            size="small"
            onClick={() => setShowAlert(false)}
          >
            <Close fontSize="inherit" />
          </IconButton>
        }
      >
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Info sx={{ mr: 1 }} />
          <Typography variant="body2">
            {hiddenCount} section{hiddenCount > 1 ? 's' : ''} hidden on this {pageName} due to empty data sets. 
            Showing {visibleSections.length} of {totalSections} available sections.
          </Typography>
        </Box>
      </Alert>
    </Collapse>
  );
};

export default DataAvailabilityIndicator;
