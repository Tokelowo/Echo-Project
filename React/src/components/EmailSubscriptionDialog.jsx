import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  Alert,
  CircularProgress,
  Grid,
  Box,
  Chip,
  FormControlLabel,
  Switch,
  InputAdornment,
} from '@mui/material';
import {
  Email as EmailIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { fetchData } from '../utils/api';

const EmailSubscriptionDialog = ({ open, onClose, pageType = 'market_trends' }) => {
  const [formData, setFormData] = useState({
    userEmail: '',
    userName: '',
    frequency: 'weekly',
    queryTemplate: '',
    agentType: pageType,
    deliveryFormat: 'email',
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone, // Auto-detect user's timezone
    preferredTime: '09:00',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const frequencyOptions = [
    { value: 'daily', label: 'Daily Reports', description: 'Get updates every day' },
    { value: 'weekly', label: 'Weekly Reports', description: 'Get updates every week' },
    { value: 'monthly', label: 'Monthly Reports', description: 'Get updates every month' },
  ];

  const agentTypeOptions = [
    { value: 'market_trends_agent', label: 'Market Trends', description: 'Industry trends and analysis' },
    { value: 'competitive_intelligence_agent', label: 'Competitive Intelligence', description: 'Competitor analysis and insights' },
    { value: 'product_intelligence_agent', label: 'Product Intelligence', description: 'Product metrics and performance' },
    { value: 'comprehensive_research', label: 'Comprehensive Research', description: 'Multi-agent comprehensive analysis' },
  ];

  const deliveryFormatOptions = [
    { value: 'email', label: 'Email Only' },
    { value: 'pdf', label: 'PDF Attachment' },
    { value: 'both', label: 'Email + PDF' },
  ];

  const timezoneOptions = [
    // Americas
    { value: 'America/New_York', label: 'Eastern Time (New York)', region: 'Americas' },
    { value: 'America/Chicago', label: 'Central Time (Chicago)', region: 'Americas' },
    { value: 'America/Denver', label: 'Mountain Time (Denver)', region: 'Americas' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (Los Angeles)', region: 'Americas' },
    { value: 'America/Phoenix', label: 'Mountain Time - Arizona (Phoenix)', region: 'Americas' },
    { value: 'America/Toronto', label: 'Eastern Time (Toronto)', region: 'Americas' },
    { value: 'America/Vancouver', label: 'Pacific Time (Vancouver)', region: 'Americas' },
    { value: 'America/Sao_Paulo', label: 'Brazil Time (São Paulo)', region: 'Americas' },
    { value: 'America/Mexico_City', label: 'Central Time (Mexico City)', region: 'Americas' },
    
    // Europe
    { value: 'Europe/London', label: 'Greenwich Mean Time (London)', region: 'Europe' },
    { value: 'Europe/Paris', label: 'Central European Time (Paris)', region: 'Europe' },
    { value: 'Europe/Berlin', label: 'Central European Time (Berlin)', region: 'Europe' },
    { value: 'Europe/Rome', label: 'Central European Time (Rome)', region: 'Europe' },
    { value: 'Europe/Madrid', label: 'Central European Time (Madrid)', region: 'Europe' },
    { value: 'Europe/Amsterdam', label: 'Central European Time (Amsterdam)', region: 'Europe' },
    { value: 'Europe/Stockholm', label: 'Central European Time (Stockholm)', region: 'Europe' },
    { value: 'Europe/Helsinki', label: 'Eastern European Time (Helsinki)', region: 'Europe' },
    { value: 'Europe/Moscow', label: 'Moscow Time (Moscow)', region: 'Europe' },
    { value: 'Europe/Dublin', label: 'Greenwich Mean Time (Dublin)', region: 'Europe' },
    
    // Asia Pacific
    { value: 'Asia/Tokyo', label: 'Japan Time (Tokyo)', region: 'Asia Pacific' },
    { value: 'Asia/Shanghai', label: 'China Time (Shanghai)', region: 'Asia Pacific' },
    { value: 'Asia/Hong_Kong', label: 'Hong Kong Time (Hong Kong)', region: 'Asia Pacific' },
    { value: 'Asia/Singapore', label: 'Singapore Time (Singapore)', region: 'Asia Pacific' },
    { value: 'Asia/Seoul', label: 'Korea Time (Seoul)', region: 'Asia Pacific' },
    { value: 'Asia/Mumbai', label: 'India Time (Mumbai)', region: 'Asia Pacific' },
    { value: 'Asia/Bangkok', label: 'Thailand Time (Bangkok)', region: 'Asia Pacific' },
    { value: 'Asia/Jakarta', label: 'Indonesia Time (Jakarta)', region: 'Asia Pacific' },
    { value: 'Australia/Sydney', label: 'Australian Eastern Time (Sydney)', region: 'Asia Pacific' },
    { value: 'Australia/Melbourne', label: 'Australian Eastern Time (Melbourne)', region: 'Asia Pacific' },
    { value: 'Australia/Perth', label: 'Australian Western Time (Perth)', region: 'Asia Pacific' },
    { value: 'Pacific/Auckland', label: 'New Zealand Time (Auckland)', region: 'Asia Pacific' },
    
    // Middle East & Africa
    { value: 'Asia/Dubai', label: 'Gulf Time (Dubai)', region: 'Middle East & Africa' },
    { value: 'Africa/Johannesburg', label: 'South Africa Time (Johannesburg)', region: 'Middle East & Africa' },
    { value: 'Africa/Cairo', label: 'Eastern European Time (Cairo)', region: 'Middle East & Africa' },
    { value: 'Asia/Jerusalem', label: 'Israel Time (Jerusalem)', region: 'Middle East & Africa' },
    
    // UTC
    { value: 'UTC', label: 'Coordinated Universal Time (UTC)', region: 'UTC' },
  ];

  const getDefaultQuery = (type) => {
    const queries = {
      market_trends_agent: 'Latest market trends and industry analysis for cybersecurity and email security',
      competitive_intelligence_agent: 'Competitive analysis of MDO vs major competitors in email security market',
      product_intelligence_agent: 'Product performance metrics and feature analysis for MDO',
      comprehensive_research: 'Comprehensive research across market trends, competition, and product intelligence',
    };
    return queries[type] || queries.comprehensive_research;
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
      ...(field === 'agentType' && { queryTemplate: getDefaultQuery(value) })
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validate required fields
    if (!formData.userEmail.trim()) {
      setError('Email address is required');
      setLoading(false);
      return;
    }

    if (!formData.userName.trim()) {
      setError('Name is required');
      setLoading(false);
      return;
    }

    try {
      const requestBody = {
        user_email: formData.userEmail,
        user_name: formData.userName,
        agent_type: formData.agentType,
        frequency: formData.frequency,
        query_template: formData.queryTemplate || getDefaultQuery(formData.agentType),
        delivery_format: formData.deliveryFormat,
        time_zone: formData.timeZone,
        preferred_time: formData.preferredTime + ':00',
        is_active: true,
      };

      // Call the subscription endpoint
      await fetchData('/subscribe-to-reports/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      setSuccess(true);
      
      // Auto-close after 2 seconds
      setTimeout(() => {
        onClose();
        setSuccess(false);
        setFormData({
          userEmail: '',
          userName: '',
          frequency: 'weekly',
          queryTemplate: '',
          agentType: pageType,
          deliveryFormat: 'email',
          timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
          preferredTime: '09:00',
        });
      }, 2000);

    } catch (err) {
      setError(err.message || 'Failed to create subscription. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      onClose();
      setError(null);
      setSuccess(false);
    }
  };

  React.useEffect(() => {
    if (open && pageType) {
      setFormData(prev => ({
        ...prev,
        agentType: pageType,
        queryTemplate: getDefaultQuery(pageType)
      }));
    }
  }, [open, pageType]);

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <EmailIcon color="primary" />
          <Typography variant="h6">Subscribe to Automated Reports</Typography>
        </Box>
      </DialogTitle>

      <DialogContent>
        {success ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <CheckCircleIcon color="success" sx={{ fontSize: 64, mb: 2 }} />
            <Typography variant="h6" color="success.main" gutterBottom>
              Subscription Created Successfully!
            </Typography>
            <Typography variant="body2" color="text.secondary">
              You'll receive your first report based on your selected schedule.
            </Typography>
          </Box>
        ) : (
          <Box component="form" onSubmit={handleSubmit}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Grid container spacing={3}>
              {/* User Information */}
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                  Contact Information
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Your Email"
                  type="email"
                  value={formData.userEmail}
                  onChange={(e) => handleInputChange('userEmail', e.target.value)}
                  required
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <EmailIcon />
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Your Name"
                  value={formData.userName}
                  onChange={(e) => handleInputChange('userName', e.target.value)}
                  required
                />
              </Grid>

              {/* Subscription Settings */}
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, mt: 2 }}>
                  Report Settings
                </Typography>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Report Type</InputLabel>
                  <Select
                    value={formData.agentType}
                    label="Report Type"
                    onChange={(e) => handleInputChange('agentType', e.target.value)}
                  >
                    {agentTypeOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        <Box>
                          <Typography variant="body2">{option.label}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {option.description}
                          </Typography>
                        </Box>
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Frequency</InputLabel>
                  <Select
                    value={formData.frequency}
                    label="Frequency"
                    onChange={(e) => handleInputChange('frequency', e.target.value)}
                  >
                    {frequencyOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        <Box>
                          <Typography variant="body2">{option.label}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {option.description}
                          </Typography>
                        </Box>
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Report Focus (Optional)"
                  multiline
                  rows={3}
                  value={formData.queryTemplate}
                  onChange={(e) => handleInputChange('queryTemplate', e.target.value)}
                  placeholder="Customize what you'd like to focus on in your reports..."
                  helperText="Leave blank to use default topics for the selected report type"
                />
              </Grid>

              {/* Delivery Settings */}
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, mt: 2 }}>
                  Delivery Settings
                </Typography>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Delivery Format</InputLabel>
                  <Select
                    value={formData.deliveryFormat}
                    label="Delivery Format"
                    onChange={(e) => handleInputChange('deliveryFormat', e.target.value)}
                  >
                    {deliveryFormatOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Time Zone</InputLabel>
                  <Select
                    value={formData.timeZone}
                    label="Time Zone"
                    onChange={(e) => handleInputChange('timeZone', e.target.value)}
                  >
                    {/* Group timezones by region */}
                    {['Americas', 'Europe', 'Asia Pacific', 'Middle East & Africa', 'UTC'].map((region) => [
                      <MenuItem key={`header-${region}`} disabled sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        {region}
                      </MenuItem>,
                      ...timezoneOptions
                        .filter(tz => tz.region === region)
                        .map((option) => (
                          <MenuItem key={option.value} value={option.value} sx={{ pl: 3 }}>
                            {option.label}
                          </MenuItem>
                        ))
                    ])}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Preferred Time"
                  type="time"
                  value={formData.preferredTime}
                  onChange={(e) => handleInputChange('preferredTime', e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <ScheduleIcon />
                      </InputAdornment>
                    ),
                  }}
                  helperText={`Time in ${formData.timeZone.replace('_', ' ')}`}
                />
              </Grid>

              {/* Preview */}
              <Grid item xs={12}>
                <Box sx={{ mt: 2, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Subscription Summary:
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip 
                      label={agentTypeOptions.find(opt => opt.value === formData.agentType)?.label} 
                      color="primary" 
                      size="small" 
                    />
                    <Chip 
                      label={frequencyOptions.find(opt => opt.value === formData.frequency)?.label} 
                      color="secondary" 
                      size="small" 
                    />
                    <Chip 
                      label={`${formData.preferredTime} ${timezoneOptions.find(tz => tz.value === formData.timeZone)?.label.split('(')[1]?.replace(')', '') || formData.timeZone}`} 
                      variant="outlined" 
                      size="small" 
                    />
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </Box>
        )}
      </DialogContent>

      {!success && (
        <DialogActions>
          <Button onClick={handleClose} disabled={loading}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <EmailIcon />}
          >
            {loading ? 'Creating Subscription...' : 'Subscribe to Reports'}
          </Button>
        </DialogActions>
      )}
    </Dialog>
  );
};

export default EmailSubscriptionDialog;
