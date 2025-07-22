import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton, 
  Box, 
  Tooltip 
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useAccessibility } from '../../contexts/AccessibilityContext';

const Header = ({ toggleDrawer }) => {
  const { announce } = useAccessibility();

  const handleMenuToggle = () => {
    toggleDrawer();
    announce('Navigation menu toggled');
  };

  return (
    <AppBar 
      position="fixed" 
      component="header"
      role="banner"
      sx={{ 
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: 'background.paper',
        color: 'text.primary',
        boxShadow: 'none',
        borderBottom: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Toolbar sx={{ minHeight: '64px !important' }}>
        <Tooltip title="Toggle navigation menu" arrow>
          <IconButton
            color="inherit"
            aria-label="Toggle navigation menu"
            onClick={handleMenuToggle}
            edge="start"
            sx={{ 
              mr: 2,
              minWidth: 44,
              minHeight: 44,
              '&:focus-visible': {
                outline: '3px solid',
                outlineColor: 'primary.main',
                outlineOffset: '2px',
              },
            }}
          >
            <MenuIcon />
          </IconButton>
        </Tooltip>
        
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <Box
            component="div"
            role="img"
            aria-label="Research Intelligence Platform logo"
            sx={{
              width: 32,
              height: 32,
              backgroundColor: 'primary.main',
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
            }}
          >
            <Typography
              variant="h6"
              sx={{
                color: 'primary.contrastText',
                fontSize: '1rem',
                fontWeight: 'bold',
              }}
              aria-hidden="true"
            >
              📊
            </Typography>
          </Box>
          <Typography 
            variant="h6" 
            component="h1" 
            sx={{ 
              fontWeight: 600,
              fontSize: '1.125rem',
              color: 'text.primary',
            }}
          >
            Research Intelligence Platform
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
