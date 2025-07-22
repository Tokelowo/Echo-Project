import React, { useState, useEffect } from 'react';
import { 
  Alert, 
  Snackbar, 
  Box,
  Typography,
  Fade,
  Paper
} from '@mui/material';
import { 
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  AccessibilityNew as AccessibilityIcon
} from '@mui/icons-material';

const AccessibilityNotifications = ({ message, type, open, onClose }) => {
  return (
    <>
      {/* Large Banner Notification */}
      <Snackbar
        open={open}
        autoHideDuration={4000}
        onClose={onClose}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        sx={{ 
          '& .MuiSnackbarContent-root': {
            minWidth: '400px',
            fontSize: '1.2rem'
          }
        }}
      >
        <Alert
          onClose={onClose}
          severity={type === 'enabled' ? 'success' : 'info'}
          variant="filled"
          icon={type === 'enabled' ? <CheckCircleIcon /> : <CancelIcon />}
          sx={{
            fontSize: '1.2rem',
            fontWeight: 'bold',
            minHeight: '60px',
            alignItems: 'center',
            boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
            transform: 'scale(1.1)',
            border: '3px solid',
            borderColor: type === 'enabled' ? '#4caf50' : '#ff9800'
          }}
        >
          {message}
        </Alert>
      </Snackbar>

      {/* Overlay Banner for Extra Visibility */}
      <Fade in={open} timeout={500}>
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 9999,
            pointerEvents: 'none'
          }}
        >
          <Paper
            elevation={8}
            className="notification-pulse"
            sx={{
              mx: 'auto',
              mt: 2,
              p: 3,
              maxWidth: '600px',
              backgroundColor: type === 'enabled' ? '#4caf50' : '#ff9800',
              color: '#fff',
              textAlign: 'center',
              border: '4px solid #fff',
              borderRadius: '12px'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2 }}>
              <AccessibilityIcon sx={{ fontSize: '2rem' }} />
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {message}
              </Typography>
              {type === 'enabled' ? 
                <CheckCircleIcon sx={{ fontSize: '2rem' }} /> : 
                <CancelIcon sx={{ fontSize: '2rem' }} />
              }
            </Box>
          </Paper>
        </Box>
      </Fade>
    </>
  );
};

export default AccessibilityNotifications;
