import React from 'react';
import {
  Box,
  Typography,
  ButtonGroup,
  Button,
  Slider,
  Card,
  CardContent,
  Chip,
  Alert
} from '@mui/material';
import { useAccessibility } from '../contexts/AccessibilityContext';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import FormatSizeIcon from '@mui/icons-material/FormatSize';

const TextSizeSelector = ({ showNotification }) => {
  const { fontSize, setFontSize } = useAccessibility();

  const textSizes = [
    { value: 90, label: 'Small', description: 'Compact text' },
    { value: 110, label: 'Normal', description: 'Default size (recommended)' },
    { value: 125, label: 'Medium', description: 'Slightly larger' },
    { value: 140, label: 'Large', description: 'Comfortable reading' },
    { value: 160, label: 'Extra Large', description: 'Maximum readability' }
  ];

  const handleSizeChange = (newSize) => {
    setFontSize(newSize);
    const sizeInfo = textSizes.find(size => size.value === newSize);
    const message = `🔤 Text size changed to ${sizeInfo.label} (${newSize}%)`;
    if (showNotification) {
      showNotification(message, 'success');
    }
  };

  const handleSliderChange = (event, newValue) => {
    setFontSize(newValue);
  };

  const getCurrentSizeInfo = () => {
    return textSizes.find(size => size.value === fontSize) || 
           { label: 'Custom', description: `${fontSize}%` };
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <TextFieldsIcon color="primary" />
          <Typography variant="h6" component="h3">
            Text Size Control
          </Typography>
          <Chip 
            label={getCurrentSizeInfo().label} 
            color="primary" 
            size="small"
          />
        </Box>

        {/* Quick Size Buttons */}
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Quick Options:
        </Typography>
        <ButtonGroup 
          variant="outlined" 
          size="small" 
          sx={{ mb: 3, flexWrap: 'wrap', gap: 1 }}
        >
          {textSizes.map((size) => (
            <Button
              key={size.value}
              onClick={() => handleSizeChange(size.value)}
              variant={fontSize === size.value ? 'contained' : 'outlined'}
              color={fontSize === size.value ? 'primary' : 'inherit'}
              sx={{ 
                minWidth: 'auto',
                fontSize: fontSize === size.value ? '1.1rem' : '0.875rem',
                fontWeight: fontSize === size.value ? 'bold' : 'normal'
              }}
            >
              {size.label}
            </Button>
          ))}
        </ButtonGroup>

        {/* Slider for Fine Control */}
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Fine Control: {fontSize}%
        </Typography>
        <Box sx={{ px: 2, mb: 2 }}>
          <Slider
            value={fontSize}
            onChange={handleSliderChange}
            min={80}
            max={180}
            step={5}
            marks={textSizes.map(size => ({ value: size.value, label: size.label.charAt(0) }))}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${value}%`}
            color="primary"
          />
        </Box>

        {/* Preview Text */}
        <Box sx={{ 
          p: 2, 
          border: '2px dashed',
          borderColor: 'divider',
          borderRadius: 1,
          bgcolor: 'grey.50',
          mb: 2
        }}>
          <Typography variant="h6" gutterBottom sx={{ fontSize: `${fontSize}%` }}>
            📖 Preview Text - {getCurrentSizeInfo().label}
          </Typography>
          <Typography variant="body1" sx={{ fontSize: `${fontSize}%` }}>
            This is how your text will look. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
            The quick brown fox jumps over the lazy dog.
          </Typography>
          <Typography variant="body2" sx={{ fontSize: `${fontSize}%`, mt: 1 }}>
            Smaller text example: {getCurrentSizeInfo().description}
          </Typography>
        </Box>

        {/* Current Status */}
        <Alert 
          severity={fontSize > 120 ? 'success' : fontSize < 100 ? 'warning' : 'info'}
          icon={<FormatSizeIcon />}
        >
          <strong>Current Setting:</strong> {getCurrentSizeInfo().label} ({fontSize}%)
          <br />
          {getCurrentSizeInfo().description}
          {fontSize > 140 && ' - Great for accessibility!'}
        </Alert>
      </CardContent>
    </Card>
  );
};

export default TextSizeSelector;
