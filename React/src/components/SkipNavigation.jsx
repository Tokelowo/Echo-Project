import React from 'react';
import { Button, Box } from '@mui/material';
import { useAccessibility } from '../contexts/AccessibilityContext';

const SkipNavigation = () => {
  const { skipToContent, announce } = useAccessibility();

  const handleSkipToContent = () => {
    skipToContent();
    announce('Skipped to main content');
  };

  const handleSkipToNav = () => {
    const navigation = document.getElementById('main-navigation');
    if (navigation) {
      navigation.focus();
      navigation.scrollIntoView({ behavior: 'smooth' });
      announce('Skipped to main navigation');
    }
  };

  return (
    <Box
      sx={{
        position: 'absolute',
        top: -40,
        left: 8,
        zIndex: 9999,
        '&:focus-within': {
          top: 8,
        },
      }}
    >
      <Button
        variant="contained"
        color="primary"
        size="small"
        onClick={handleSkipToContent}
        onFocus={(e) => {
          e.target.parentElement.style.top = '8px';
        }}
        onBlur={(e) => {
          e.target.parentElement.style.top = '-40px';
        }}
        sx={{
          mr: 1,
          fontSize: '0.875rem',
          fontWeight: 600,
          '&:focus-visible': {
            outline: '3px solid',
            outlineColor: 'primary.light',
            outlineOffset: '2px',
          },
        }}
      >
        Skip to main content
      </Button>
      <Button
        variant="outlined"
        color="primary"
        size="small"
        onClick={handleSkipToNav}
        onFocus={(e) => {
          e.target.parentElement.style.top = '8px';
        }}
        onBlur={(e) => {
          e.target.parentElement.style.top = '-40px';
        }}
        sx={{
          fontSize: '0.875rem',
          fontWeight: 600,
          '&:focus-visible': {
            outline: '3px solid',
            outlineColor: 'primary.light',
            outlineOffset: '2px',
          },
        }}
      >
        Skip to navigation
      </Button>
    </Box>
  );
};

export default SkipNavigation;
