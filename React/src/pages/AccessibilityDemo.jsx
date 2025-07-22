import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemText,
  Chip,
  Alert,
  AlertTitle,
  Grid,
  Paper,
  Stack,
} from '@mui/material';
import { useAccessibility } from '../contexts/AccessibilityContext';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import ContrastIcon from '@mui/icons-material/Contrast';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import AccessibilityNotifications from '../components/AccessibilityNotifications';
import TextSizeSelector from '../components/TextSizeSelector';

const AccessibilityDemo = () => {
  const [notification, setNotification] = useState({ open: false, message: '', type: '' });
  
  const { 
    darkMode, 
    highContrast, 
    reducedMotion,
    fontSize,
    speechEnabled,
    announce, 
    stopSpeech,
    setDarkMode, 
    setHighContrast,
    setSpeechEnabled
  } = useAccessibility();

  const showNotification = (message, type) => {
    setNotification({ open: true, message, type });
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const handleTestAnnouncement = () => {
    const messages = [
      'Screen reader test successful! This message was announced.',
      'Accessibility features are working properly.',
      'Screen readers will announce dynamic content changes.'
    ];
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    announce(randomMessage, 'assertive');
    showNotification(`📢 Announced: "${randomMessage}"`, 'success');
  };

  const handleToggleDarkMode = () => {
    const newValue = !darkMode;
    setDarkMode(newValue);
    const message = `🌙 Dark Mode ${newValue ? 'ENABLED' : 'DISABLED'}! Look at the page colors change!`;
    announce(message);
    showNotification(message, newValue ? 'enabled' : 'disabled');
  };

  const handleToggleHighContrast = () => {
    const newValue = !highContrast;
    setHighContrast(newValue);
    const message = `⚡ High Contrast ${newValue ? 'ENABLED' : 'DISABLED'}! Notice the dramatic visual changes!`;
    announce(message);
    showNotification(message, newValue ? 'enabled' : 'disabled');
  };

  const accessibilityFeatures = [
    {
      name: 'Dark Mode',
      status: darkMode ? 'Enabled' : 'Disabled',
      description: 'Reduces eye strain in low-light environments',
    },
    {
      name: 'High Contrast',
      status: highContrast ? 'Enabled' : 'Disabled',
      description: 'Improves text visibility for users with visual impairments',
    },
    {
      name: 'Text Size',
      status: fontSize > 120 ? 'Large' : fontSize > 100 ? 'Medium' : 'Normal',
      description: `Current size: ${fontSize}% - ${fontSize > 120 ? 'Great for accessibility!' : fontSize < 100 ? 'Compact view' : 'Standard reading'}`,
    },
    {
      name: 'Reduced Motion',
      status: reducedMotion ? 'Enabled' : 'Disabled',
      description: 'Minimizes animations for users with vestibular disorders',
    },
  ];

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <AccessibilityNewIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h3" component="h1" gutterBottom>
          Accessibility Features Demo
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This page demonstrates the comprehensive accessibility features implemented in the application.
        </Typography>
      </Box>

      {/* Status Indicators */}
      <Paper 
        elevation={3} 
        sx={{ 
          p: 3, 
          mb: 4, 
          backgroundColor: theme => theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.8)' : 'rgba(255,255,255,0.95)',
          border: theme => `3px solid ${theme.palette.primary.main}`,
          borderRadius: 2
        }}
      >
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', textAlign: 'center' }}>
          🚀 Current Accessibility Status
        </Typography>
        <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap" useFlexGap>
          <Chip
            icon={darkMode ? <CheckCircleIcon /> : <RadioButtonUncheckedIcon />}
            label={`Dark Mode: ${darkMode ? 'ON' : 'OFF'}`}
            color={darkMode ? 'success' : 'default'}
            size="large"
            sx={{ 
              fontSize: '1.2rem', 
              fontWeight: 'bold',
              minWidth: '150px',
              backgroundColor: darkMode ? '#4caf50' : '#e0e0e0'
            }}
          />
          <Chip
            icon={highContrast ? <CheckCircleIcon /> : <RadioButtonUncheckedIcon />}
            label={`High Contrast: ${highContrast ? 'ON' : 'OFF'}`}
            color={highContrast ? 'success' : 'default'}
            size="large"
            sx={{ 
              fontSize: '1.2rem', 
              fontWeight: 'bold',
              minWidth: '180px',
              backgroundColor: highContrast ? '#4caf50' : '#e0e0e0'
            }}
          />
          <Chip
            icon={fontSize > 120 ? <CheckCircleIcon /> : <RadioButtonUncheckedIcon />}
            label={`Text Size: ${fontSize}%`}
            color={fontSize > 120 ? 'success' : fontSize > 100 ? 'primary' : 'default'}
            size="large"
            sx={{ 
              fontSize: '1.2rem', 
              fontWeight: 'bold',
              minWidth: '150px',
              backgroundColor: fontSize > 120 ? '#4caf50' : fontSize > 100 ? '#2196f3' : '#e0e0e0'
            }}
          />
        </Stack>
      </Paper>

      <Alert severity="info" sx={{ mb: 4 }}>
        <AlertTitle>Accessibility Toolbar</AlertTitle>
        Look for the accessibility button in the top-right corner to adjust your preferences!
      </Alert>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Current Settings
              </Typography>
              <List>
                {accessibilityFeatures.map((feature) => (
                  <ListItem key={feature.name} divider>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body1">{feature.name}</Typography>
                          <Chip
                            label={feature.status}
                            color={feature.status === 'Enabled' ? 'success' : 'default'}
                            size="small"
                          />
                        </Box>
                      }
                      secondary={feature.description}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Accessibility Features
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Keyboard Navigation
                  </Typography>
                  <Typography variant="body2">
                    • Tab through interactive elements
                    <br />
                    • Use Alt + A to open accessibility menu
                    <br />
                    • Arrow keys for navigation in menus
                  </Typography>
                </Paper>

                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Screen Reader Support
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    • Proper ARIA labels and roles
                    <br />
                    • Live announcements for dynamic content
                    <br />
                    • Semantic HTML structure
                    <br />
                    • Focus management and keyboard navigation
                  </Typography>
                  
                  <Alert severity="info" sx={{ mb: 2 }}>
                    <strong>Screen Reader Testing:</strong> This app includes aria-live regions for announcements. 
                    When you click the test button, you should:
                    <br />• See a blue notification popup (visual confirmation)
                    <br />• Hear speech synthesis (if browser supports it)
                    <br />• Screen readers will announce the message (if running)
                  </Alert>
                  
                  <Alert severity="warning" sx={{ mb: 2 }}>
                    <strong>🎧 Speech Control:</strong> Browser speech is currently <strong>{speechEnabled ? 'ENABLED' : 'DISABLED'}</strong>. 
                    Use the controls below to enable/disable or stop speech.
                  </Alert>
                  
                  {/* Speech Controls */}
                  <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      🎚️ Speech Controls:
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Button
                        variant={speechEnabled ? 'contained' : 'outlined'}
                        color={speechEnabled ? 'success' : 'primary'}
                        size="small"
                        onClick={() => {
                          setSpeechEnabled(!speechEnabled);
                          showNotification(`🔊 Speech ${!speechEnabled ? 'enabled' : 'disabled'}`, 'info');
                        }}
                      >
                        {speechEnabled ? '🔊 Speech ON' : '🔇 Speech OFF'}
                      </Button>
                      
                      <Button
                        variant="outlined"
                        color="error"
                        size="small"
                        onClick={() => {
                          stopSpeech();
                          showNotification('⏹️ All speech stopped', 'info');
                        }}
                      >
                        ⏹️ Stop Speech
                      </Button>
                    </Box>
                  </Box>
                  
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Button
                      variant="contained"
                      onClick={handleTestAnnouncement}
                      sx={{ 
                        bgcolor: 'success.main',
                        '&:hover': { bgcolor: 'success.dark' }
                      }}
                      aria-label="Test screen reader announcement - will announce a random test message"
                    >
                      🔊 Test Screen Reader
                    </Button>
                    
                    <Button
                      variant="outlined"
                      color="info"
                      onClick={() => {
                        if ('speechSynthesis' in window) {
                          const testMessage = "Speech synthesis is working! This is a browser speech test.";
                          const utterance = new SpeechSynthesisUtterance(testMessage);
                          speechSynthesis.speak(utterance);
                          showNotification('🗣️ Browser speech synthesis test played', 'success');
                        } else {
                          showNotification('❌ Speech synthesis not supported in this browser', 'error');
                        }
                      }}
                      aria-label="Test browser speech synthesis directly"
                    >
                      🗣️ Test Browser Speech
                    </Button>
                    
                    <Button
                      variant="outlined"
                      onClick={() => {
                        announce('Navigation announcement: You are currently on the Accessibility Demo page', 'polite');
                        showNotification('📍 Location announced to screen readers', 'info');
                      }}
                      aria-label="Announce current page location"
                    >
                      📍 Announce Location
                    </Button>
                    
                    <Button
                      variant="outlined"
                      onClick={() => {
                        const statusMessage = `Current settings: Dark mode ${darkMode ? 'enabled' : 'disabled'}, High contrast ${highContrast ? 'enabled' : 'disabled'}, Text size ${fontSize}%`;
                        announce(statusMessage, 'polite');
                        showNotification('⚙️ Settings announced to screen readers', 'info');
                      }}
                      aria-label="Announce current accessibility settings"
                    >
                      ⚙️ Announce Settings
                    </Button>
                  </Box>
                </Paper>

                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Try Dark Mode
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    Watch the entire interface change colors!
                  </Typography>
                  <Button
                    variant="contained"
                    onClick={handleToggleDarkMode}
                    className={darkMode ? 'accessibility-demo-active' : ''}
                    sx={{ 
                      mt: 1, 
                      mr: 1,
                      backgroundColor: darkMode ? '#4caf50' : 'primary.main',
                      color: '#fff',
                      fontWeight: 'bold',
                      fontSize: '1.1rem',
                      minHeight: '48px',
                      border: darkMode ? '3px solid #2e7d32' : 'none',
                      '&:hover': {
                        backgroundColor: darkMode ? '#388e3c' : 'primary.dark',
                        transform: 'scale(1.05)'
                      }
                    }}
                    startIcon={darkMode ? <LightModeIcon /> : <DarkModeIcon />}
                  >
                    {darkMode ? '🌞 Switch to Light Mode' : '🌙 Switch to Dark Mode'}
                  </Button>
                </Paper>

                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Try High Contrast
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    See enhanced contrast for better visibility!
                  </Typography>
                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={handleToggleHighContrast}
                    className={highContrast ? 'accessibility-demo-active' : ''}
                    sx={{ 
                      mt: 1,
                      backgroundColor: highContrast ? '#4caf50' : 'secondary.main',
                      color: '#fff',
                      fontWeight: 'bold',
                      fontSize: '1.1rem',
                      minHeight: '48px',
                      border: highContrast ? '3px solid #2e7d32' : 'none',
                      '&:hover': {
                        backgroundColor: highContrast ? '#388e3c' : 'secondary.dark',
                        transform: 'scale(1.05)'
                      }
                    }}
                    startIcon={<ContrastIcon />}
                  >
                    {highContrast ? '⚡ Disable High Contrast' : '⚡ Enable High Contrast'}
                  </Button>
                </Paper>

                {/* Text Size Control - New Advanced Component */}
                <TextSizeSelector showNotification={showNotification} />

                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Visual Accessibility
                  </Typography>
                  <Typography variant="body2">
                    • WCAG 2.1 AA compliant color contrast
                    <br />
                    • Focus indicators on all interactive elements
                    <br />
                    • Scalable text and interface elements
                  </Typography>
                </Paper>

                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Motor Accessibility
                  </Typography>
                  <Typography variant="body2">
                    • Minimum 44px touch targets
                    <br />
                    • No time-based interactions
                    <br />
                    • Multiple ways to interact with content
                  </Typography>
                </Paper>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Accessibility Notifications */}
      <AccessibilityNotifications
        message={notification.message}
        type={notification.type}
        open={notification.open}
        onClose={handleCloseNotification}
      />
    </Box>
  );
};

export default AccessibilityDemo;
