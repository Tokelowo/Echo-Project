import React from 'react';
import { Box, Chip, Typography, Tooltip } from '@mui/material';
import { 
  CheckCircle, 
  Warning, 
  Info, 
  Science,
  DataUsage,
  TrendingUp 
} from '@mui/icons-material';

const DataQualityIndicator = ({ 
  dataType = 'mixed', 
  lastUpdated = null, 
  sources = [], 
  confidence = 85,
  showDetails = true 
}) => {
  const getIndicatorConfig = (type) => {
    switch (type) {
      case 'real':
        return {
          icon: <CheckCircle />,
          color: 'success',
          label: 'Real Data',
          description: 'Live data from production systems and APIs',
          bgColor: '#e8f5e8'
        };
      case 'demo':
        return {
          icon: <Science />,
          color: 'info',
          label: 'Demo Data',
          description: 'Simulated data for demonstration purposes',
          bgColor: '#e3f2fd'
        };
      case 'mixed':
        return {
          icon: <DataUsage />,
          color: 'warning',
          label: 'Mixed Data',
          description: 'Combination of real and simulated data',
          bgColor: '#fff3e0'
        };
      case 'simulated':
        return {
          icon: <TrendingUp />,
          color: 'secondary',
          label: 'Simulated',
          description: 'AI-generated realistic data based on patterns',
          bgColor: '#f3e5f5'
        };
      default:
        return {
          icon: <Info />,
          color: 'default',
          label: 'Unknown',
          description: 'Data source not specified',
          bgColor: '#f5f5f5'
        };
    }
  };

  const config = getIndicatorConfig(dataType);

  return (
    <Box sx={{ mb: 2 }}>
      <Box 
        sx={{ 
          p: 2, 
          backgroundColor: config.bgColor, 
          borderRadius: 1,
          border: `1px solid ${config.color === 'success' ? '#4caf50' : 
                                config.color === 'warning' ? '#ff9800' : 
                                config.color === 'info' ? '#2196f3' : '#9c27b0'}20`
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Tooltip title={config.description}>
            <Chip
              icon={config.icon}
              label={config.label}
              color={config.color}
              size="small"
              variant="outlined"
            />
          </Tooltip>
          
          {confidence && (
            <Chip
              label={`${confidence}% Confidence`}
              color={confidence > 90 ? 'success' : confidence > 70 ? 'warning' : 'error'}
              size="small"
              variant="outlined"
            />
          )}
        </Box>

        {showDetails && (
          <Box>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
              {config.description}
            </Typography>
            
            {lastUpdated && (
              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                Last updated: {new Date(lastUpdated).toLocaleString()}
              </Typography>
            )}
            
            {sources && sources.length > 0 && (
              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                Sources: {sources.join(', ')}
              </Typography>
            )}
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default DataQualityIndicator;
