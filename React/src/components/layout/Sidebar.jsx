import React from 'react';
import { 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  Toolbar,
  Box,
  Typography,
  Divider,
  ListItemButton,
  Chip,
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import CompareIcon from '@mui/icons-material/Compare';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import InsightsIcon from '@mui/icons-material/Insights';
import SettingsIcon from '@mui/icons-material/Settings';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAccessibility } from '../../contexts/AccessibilityContext';

const drawerWidth = 280;

const menuItems = [
  { 
    text: 'Overview', 
    icon: <DashboardIcon />, 
    path: '/',
    description: 'Dashboard & insights'
  },
  { 
    text: 'Competitive Intelligence', 
    icon: <CompareIcon />, 
    path: '/competitors',
    description: 'Market analysis & competitors',
    badge: 'AI'
  },
  { 
    text: 'Product Intelligence', 
    icon: <InsightsIcon />, 
    path: '/intelligence',
    description: 'MDO capabilities & features',
    badge: 'AI'
  },
  { 
    text: 'Market Trends', 
    icon: <TrendingUpIcon />, 
    path: '/market',
    description: 'Industry trends & analysis',
    badge: 'AI'
  },
  { 
    text: 'Manage Subscriptions', 
    icon: <SettingsIcon />, 
    path: '/subscriptions',
    description: 'Email subscription settings'
  },
  { 
    text: 'Accessibility', 
    icon: <AccessibilityNewIcon />, 
    path: '/accessibility',
    description: 'Accessibility features demo'
  },
];

const Sidebar = ({ open }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { announce } = useAccessibility();

  const isActive = (path) => location.pathname === path;

  const handleNavigation = (item) => {
    navigate(item.path);
    announce(`Navigated to ${item.text} page`);
  };

  // Handle keyboard navigation
  const handleKeyDown = (event, item) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleNavigation(item);
    }
  };

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      component="nav"
      aria-label="Main navigation"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          backgroundColor: '#f3f2f1',
          borderRight: '1px solid #e1dfdd',
        },
      }}
    >
      <Toolbar />
      
      {/* Main Navigation */}
      <Box sx={{ px: 2, py: 1 }}>
        <Typography 
          variant="overline" 
          component="h2"
          sx={{ 
            color: '#605e5c', 
            fontWeight: 600, 
            fontSize: '0.75rem',
            letterSpacing: '0.5px'
          }}
        >
          Research Intelligence
        </Typography>
      </Box>
      
      <List 
        sx={{ px: 1, py: 1 }}
        component="ul"
        role="list"
        aria-label="Main navigation menu"
      >
        {menuItems.map((item, index) => (
          <ListItemButton
            key={item.text}
            component="li"
            role="menuitem"
            tabIndex={0}
            onClick={() => handleNavigation(item)}
            onKeyDown={(e) => handleKeyDown(e, item)}
            aria-current={isActive(item.path) ? 'page' : undefined}
            aria-label={`${item.text}: ${item.description}${item.badge ? ` (${item.badge})` : ''}`}
            sx={{
              borderRadius: 1,
              mb: 1,
              mx: 0,
              px: 2,
              py: 1.5,
              minHeight: 64,
              backgroundColor: isActive(item.path) ? '#e3f2fd' : 'transparent',
              border: isActive(item.path) ? '1px solid #0078d4' : '1px solid transparent',
              '&:hover': {
                backgroundColor: isActive(item.path) ? '#e3f2fd' : '#edebe9',
              },
              '&:focus-visible': {
                outline: '3px solid #0078d4',
                outlineOffset: '2px',
              },
            }}
          >
            <ListItemIcon 
              sx={{ 
                color: isActive(item.path) ? '#0078d4' : '#605e5c',
                minWidth: 48,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
              aria-hidden="true"
            >
              {item.icon}
            </ListItemIcon>
            <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.5 }}>
                <Typography 
                  variant="body2" 
                  sx={{ 
                    fontWeight: isActive(item.path) ? 600 : 500,
                    color: isActive(item.path) ? '#0078d4' : '#323130',
                    fontSize: '0.875rem',
                    lineHeight: 1.2
                  }}
                >
                  {item.text}
                </Typography>
                {item.badge && (
                  <Chip
                    label={item.badge}
                    size="small"
                    sx={{
                      height: 18,
                      fontSize: '0.625rem',
                      backgroundColor: '#107c10',
                      color: 'white',
                      fontWeight: 600,
                      ml: 1
                    }}
                  />
                )}
              </Box>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: '#605e5c',
                  fontSize: '0.75rem',
                  lineHeight: 1.2,
                  display: 'block'
                }}
              >
                {item.description}
              </Typography>
            </Box>
          </ListItemButton>
        ))}      </List>
    </Drawer>
  );
};

export default Sidebar;
export { drawerWidth };
