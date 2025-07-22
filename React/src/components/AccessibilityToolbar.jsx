import React, { useState } from 'react';
import {
  Box,
  Button,
  Drawer,
  Typography,
  Switch,
  Slider,
  FormControlLabel,
  Divider,
  IconButton,
  Tooltip,
  Stack,
  Card,
  CardContent,
  Chip,
  Alert,
} from '@mui/material';
import {
  Accessibility as AccessibilityIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon,
  Contrast as ContrastIcon,
  TextFields as TextFieldsIcon,
  Keyboard as KeyboardIcon,
  VolumeUp as VolumeUpIcon,
  Close as CloseIcon,
  RestartAlt as RestartAltIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useAccessibility } from '../contexts/AccessibilityContext';

const AccessibilityToolbar = () => {
  const [open, setOpen] = useState(false);
  const {
    darkMode,
    setDarkMode,
    highContrast,
    setHighContrast,
    reducedMotion,
    setReducedMotion,
    fontSize,
    setFontSize,
    dyslexiaFont,
    setDyslexiaFont,
    screenReaderMode,
    setScreenReaderMode,
    keyboardNavigation,
    announce,
  } = useAccessibility();

  const handleToggleDrawer = () => {
    setOpen(!open);
    announce(open ? 'Accessibility menu closed' : 'Accessibility menu opened');
  };

  const handleReset = () => {
    setDarkMode(false);
    setHighContrast(false);
    setReducedMotion(false);
    setFontSize(100);
    setDyslexiaFont(false);
    setScreenReaderMode(false);
    announce('Accessibility settings reset to defaults');
  };

  const getFontSizeLabel = (value) => {
    if (value < 100) return 'Small';
    if (value > 100) return 'Large';
    return 'Normal';
  };

  return (
    <>
      {/* Accessibility toolbar button */}
      <Tooltip title="Open accessibility options" arrow>
        <IconButton
          onClick={handleToggleDrawer}
          sx={{
            position: 'fixed',
            bottom: 20,
            right: 20,
            zIndex: 1300,
            backgroundColor: 'primary.main',
            color: 'primary.contrastText',
            width: 56,
            height: 56,
            '&:hover': {
              backgroundColor: 'primary.dark',
              transform: 'scale(1.1)',
            },
            '&:focus-visible': {
              outline: '3px solid',
              outlineColor: 'primary.light',
              outlineOffset: '2px',
            },
            boxShadow: 3,
            transition: 'all 0.2s ease-in-out',
          }}
          aria-label="Open accessibility settings"
        >
          <AccessibilityIcon fontSize="large" />
        </IconButton>
      </Tooltip>

      {/* Accessibility settings drawer */}
      <Drawer
        anchor="right"
        open={open}
        onClose={handleToggleDrawer}
        sx={{
          '& .MuiDrawer-paper': {
            width: { xs: '100%', sm: 400 },
            maxWidth: 400,
            padding: 2,
          },
        }}
        role="dialog"
        aria-labelledby="accessibility-settings-title"
        aria-describedby="accessibility-settings-description"
      >
        <Box>
          {/* Header */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Typography
              id="accessibility-settings-title"
              variant="h5"
              component="h2"
              sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}
            >
              <AccessibilityIcon />
              Accessibility
            </Typography>
            <IconButton
              onClick={handleToggleDrawer}
              aria-label="Close accessibility settings"
              sx={{
                '&:focus-visible': {
                  outline: '3px solid',
                  outlineColor: 'primary.main',
                  outlineOffset: '2px',
                },
              }}
            >
              <CloseIcon />
            </IconButton>
          </Box>

          <Typography
            id="accessibility-settings-description"
            variant="body2"
            color="text.secondary"
            sx={{ mb: 3 }}
          >
            Customize your experience to make the application more accessible and comfortable to use.
          </Typography>

          {/* Quick actions */}
          <Card sx={{ mb: 3, backgroundColor: 'background.elevated' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                <Chip
                  icon={darkMode ? <LightModeIcon /> : <DarkModeIcon />}
                  label={darkMode ? 'Light Mode' : 'Dark Mode'}
                  onClick={() => {
                    setDarkMode(!darkMode);
                    announce(`Switched to ${!darkMode ? 'dark' : 'light'} mode`);
                  }}
                  color={darkMode ? "default" : "primary"}
                  variant={darkMode ? "outlined" : "filled"}
                />
                <Chip
                  icon={<ContrastIcon />}
                  label="High Contrast"
                  onClick={() => {
                    setHighContrast(!highContrast);
                    announce(`High contrast ${!highContrast ? 'enabled' : 'disabled'}`);
                  }}
                  color={highContrast ? "primary" : "default"}
                  variant={highContrast ? "filled" : "outlined"}
                />
                <Chip
                  icon={<RestartAltIcon />}
                  label="Reset All"
                  onClick={handleReset}
                  color="secondary"
                  variant="outlined"
                />
              </Stack>
            </CardContent>
          </Card>

          {/* Display settings */}
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <DarkModeIcon />
            Display
          </Typography>

          <FormControlLabel
            control={
              <Switch
                checked={darkMode}
                onChange={(e) => {
                  setDarkMode(e.target.checked);
                  announce(`Dark mode ${e.target.checked ? 'enabled' : 'disabled'}`);
                }}
                inputProps={{ 'aria-describedby': 'dark-mode-description' }}
              />
            }
            label="Dark mode"
            sx={{ mb: 1 }}
          />
          <Typography id="dark-mode-description" variant="caption" color="text.secondary" sx={{ mb: 2, display: 'block' }}>
            Reduces eye strain in low-light environments
          </Typography>

          <FormControlLabel
            control={
              <Switch
                checked={highContrast}
                onChange={(e) => {
                  setHighContrast(e.target.checked);
                  announce(`High contrast ${e.target.checked ? 'enabled' : 'disabled'}`);
                }}
                inputProps={{ 'aria-describedby': 'contrast-description' }}
              />
            }
            label="High contrast"
            sx={{ mb: 1 }}
          />
          <Typography id="contrast-description" variant="caption" color="text.secondary" sx={{ mb: 2, display: 'block' }}>
            Increases contrast between text and background
          </Typography>

          <FormControlLabel
            control={
              <Switch
                checked={reducedMotion}
                onChange={(e) => {
                  setReducedMotion(e.target.checked);
                  announce(`Reduced motion ${e.target.checked ? 'enabled' : 'disabled'}`);
                }}
                inputProps={{ 'aria-describedby': 'motion-description' }}
              />
            }
            label="Reduce motion"
            sx={{ mb: 1 }}
          />
          <Typography id="motion-description" variant="caption" color="text.secondary" sx={{ mb: 3, display: 'block' }}>
            Minimizes animations and transitions
          </Typography>

          <Divider sx={{ my: 3 }} />

          {/* Text settings */}
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TextFieldsIcon />
            Text & Reading
          </Typography>

          <Typography gutterBottom>
            Font size: {getFontSizeLabel(fontSize)} ({fontSize}%)
          </Typography>
          <Slider
            value={fontSize}
            onChange={(e, value) => {
              setFontSize(value);
              announce(`Font size changed to ${getFontSizeLabel(value)}`);
            }}
            min={75}
            max={150}
            step={25}
            marks={[
              { value: 75, label: 'Small' },
              { value: 100, label: 'Normal' },
              { value: 125, label: 'Large' },
              { value: 150, label: 'Extra Large' },
            ]}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${value}%`}
            aria-label="Font size"
            sx={{ mb: 3 }}
          />

          <FormControlLabel
            control={
              <Switch
                checked={dyslexiaFont}
                onChange={(e) => {
                  setDyslexiaFont(e.target.checked);
                  announce(`Dyslexia-friendly font ${e.target.checked ? 'enabled' : 'disabled'}`);
                }}
                inputProps={{ 'aria-describedby': 'dyslexia-font-description' }}
              />
            }
            label="Dyslexia-friendly font"
            sx={{ mb: 1 }}
          />
          <Typography id="dyslexia-font-description" variant="caption" color="text.secondary" sx={{ mb: 3, display: 'block' }}>
            Uses OpenDyslexic font for improved readability
          </Typography>

          <Divider sx={{ my: 3 }} />

          {/* Navigation settings */}
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <KeyboardIcon />
            Navigation
          </Typography>

          <FormControlLabel
            control={
              <Switch
                checked={screenReaderMode}
                onChange={(e) => {
                  setScreenReaderMode(e.target.checked);
                  announce(`Screen reader mode ${e.target.checked ? 'enabled' : 'disabled'}`);
                }}
                inputProps={{ 'aria-describedby': 'screen-reader-description' }}
              />
            }
            label="Screen reader optimizations"
            sx={{ mb: 1 }}
          />
          <Typography id="screen-reader-description" variant="caption" color="text.secondary" sx={{ mb: 2, display: 'block' }}>
            Enhances compatibility with screen readers
          </Typography>

          {keyboardNavigation && (
            <Alert severity="info" sx={{ mb: 2 }}>
              <Typography variant="body2">
                Keyboard navigation detected. Use Tab to move between elements and Enter/Space to activate.
              </Typography>
            </Alert>
          )}

          <Divider sx={{ my: 3 }} />

          {/* Information */}
          <Card sx={{ backgroundColor: 'background.elevated' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <InfoIcon />
                Accessibility Help
              </Typography>
              <Typography variant="body2" paragraph>
                These settings are saved automatically and will persist across sessions.
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Keyboard shortcuts:</strong>
              </Typography>
              <Typography variant="caption" component="div">
                • Tab: Navigate between elements<br />
                • Enter/Space: Activate buttons and links<br />
                • Escape: Close dialogs and menus<br />
                • Alt + A: Open this accessibility menu
              </Typography>
            </CardContent>
          </Card>

          {/* Reset button */}
          <Button
            fullWidth
            variant="outlined"
            onClick={handleReset}
            startIcon={<RestartAltIcon />}
            sx={{ mt: 3 }}
          >
            Reset All Settings
          </Button>
        </Box>
      </Drawer>
    </>
  );
};

export default AccessibilityToolbar;
