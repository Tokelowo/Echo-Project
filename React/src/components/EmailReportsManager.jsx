import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  CircularProgress,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Switch,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {  Send as SendIcon,
  Email as EmailIcon,
  Schedule as ScheduleIcon,
  Psychology as IntelligenceIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { fetchResearchAgentData } from '../utils/reportExport';

const EmailReportsManager = () => {  const [formData, setFormData] = useState({
    query: '',
    agentType: 'comprehensive_research',
    userEmail: '',
    userName: '',
    focusAreas: [],
    deliveryFormat: 'email',
    scheduleType: 'immediate',
    enableEmailDelivery: true
  });
  
  const [currentFocusArea, setCurrentFocusArea] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const agentTypes = [
    {
      value: 'comprehensive_research',
      label: 'Comprehensive Multi-Agent Research',
      description: 'All three agents collaborate for complete analysis across competitive intelligence, product intelligence, and market trends',
      icon: <CheckCircleIcon sx={{ color: '#d83b01' }} />,
      isMultiAgent: true
    },
    {
      value: 'competitive_intelligence_agent',
      label: 'Competitive Intelligence',
      description: 'Track competitors, market positioning, and competitive threats',
      icon: <IntelligenceIcon sx={{ color: '#0078d4' }} />
    },
    {
      value: 'product_intelligence_agent',
      label: 'Product Intelligence',
      description: 'Analyze product performance, features, and customer feedback',
      icon: <AssessmentIcon sx={{ color: '#107c10' }} />
    },
    {
      value: 'market_trends_agent',
      label: 'Market Trends',
      description: 'Monitor industry trends, emerging threats, and market dynamics',
      icon: <TrendingUpIcon sx={{ color: '#8a2be2' }} />
    }
  ];

  const deliveryFormats = [
    { value: 'email', label: 'Email Only' },
    { value: 'pdf', label: 'PDF Attachment' },
    { value: 'docx', label: 'Word Document' },
    { value: 'both', label: 'Email + Attachment' }
  ];

  const scheduleTypes = [
    { value: 'immediate', label: 'Send Immediately' },
    { value: 'daily', label: 'Daily Reports' },
    { value: 'weekly', label: 'Weekly Reports' },
    { value: 'monthly', label: 'Monthly Reports' }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addFocusArea = () => {
    if (currentFocusArea.trim() && !formData.focusAreas.includes(currentFocusArea.trim())) {
      setFormData(prev => ({
        ...prev,
        focusAreas: [...prev.focusAreas, currentFocusArea.trim()]
      }));
      setCurrentFocusArea('');
    }
  };

  const removeFocusArea = (area) => {
    setFormData(prev => ({
      ...prev,
      focusAreas: prev.focusAreas.filter(fa => fa !== area)
    }));
  };  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Validate required fields
    if (!formData.query.trim()) {
      setError('Research query is required');
      setLoading(false);
      return;
    }

    if (formData.enableEmailDelivery && !formData.userEmail.trim()) {
      setError('Email address is required when email delivery is enabled');
      setLoading(false);
      return;
    }

    try {
      // Use the pipeline endpoint for all agent types since it handles email delivery
      const endpoint = '/pipeline/';

      const requestBody = {
        input: formData.query,
        agent_type: formData.agentType,
        user_email: formData.enableEmailDelivery ? formData.userEmail : null,
        user_name: formData.userName || 'Research User',
        focus_areas: formData.focusAreas,
        delivery: {
          format: formData.deliveryFormat,
          schedule: formData.scheduleType
        }
      };

      const response = await fetchResearchAgentData(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });      setResult(response);    } catch (err) {
      setError(err.message || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const selectedAgent = agentTypes.find(agent => agent.value === formData.agentType);
  return (
    <Box sx={{ 
      maxWidth: 1200, 
      mx: 'auto', 
      p: 3,
      backgroundColor: '#faf9f8',
      minHeight: '100vh'
    }}>
      {/* Header */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 600, 
            color: '#323130',
            mb: 1
          }}
        >
          AI Research Reports Manager
        </Typography>
        <Typography 
          variant="h6" 
          sx={{ 
            color: '#605e5c', 
            fontWeight: 400,
            mb: 3
          }}
        >
          Generate intelligent insights and schedule automated delivery
        </Typography>
        
        {/* Status Alert */}
        <Alert 
          severity="info" 
          icon={<EmailIcon />}
          sx={{ 
            mb: 3, 
            backgroundColor: '#e3f2fd', 
            border: '1px solid #0078d4',
            maxWidth: 600,
            mx: 'auto'
          }}
        >
          Configure your research parameters and delivery preferences below. Reports will be generated using AI agents and delivered to your specified email.
        </Alert>
      </Box>
      
      <Grid container spacing={3}>
        {/* Main Form */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ 
            p: 4, 
            border: '1px solid #e1dfdd',
            boxShadow: 'none',
            borderRadius: 2
          }}>
            <Box display="flex" alignItems="center" mb={3}>
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  backgroundColor: '#0078d4',
                  borderRadius: 1,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mr: 2,
                }}
              >
                <Typography sx={{ color: 'white', fontSize: '1.25rem' }}>⚙️</Typography>
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 600, color: '#323130' }}>
                  Report Configuration
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Set up your research parameters and delivery options
                </Typography>
              </Box>
            </Box>
              
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
              {/* Agent Selection */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: '#323130' }}>
                  Select Research Agent
                </Typography>
                <FormControl fullWidth>
                  <Select
                    value={formData.agentType}
                    onChange={(e) => handleInputChange('agentType', e.target.value)}
                    displayEmpty
                    sx={{
                      backgroundColor: 'white',
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#e1dfdd',
                      },
                    }}
                  >
                    {agentTypes.map((agent) => (
                      <MenuItem key={agent.value} value={agent.value}>
                        <Box display="flex" alignItems="center">
                          {agent.icon}
                          <Box sx={{ ml: 2 }}>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {agent.label}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {agent.description}
                            </Typography>
                          </Box>
                        </Box>
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>

              {/* Research Query */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: '#323130' }}>
                  Research Query
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={formData.query}
                  onChange={(e) => handleInputChange('query', e.target.value)}
                  placeholder="What would you like to research? e.g., 'Latest Proofpoint product updates and pricing changes'"
                  required
                  sx={{
                    backgroundColor: 'white',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#e1dfdd',
                    },
                  }}
                />
              </Box>

              {/* Focus Areas */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: '#323130' }}>
                  Focus Areas <Chip label="Optional" size="small" sx={{ ml: 1 }} />
                </Typography>
                <Box display="flex" gap={1} mb={2}>
                  <TextField
                    size="small"
                    value={currentFocusArea}
                    onChange={(e) => setCurrentFocusArea(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addFocusArea())}
                    placeholder="e.g., Pricing, Features, Security"
                    sx={{ 
                      flexGrow: 1,
                      backgroundColor: 'white',
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#e1dfdd',
                      },
                    }}
                  />
                  <Button 
                    onClick={addFocusArea} 
                    variant="outlined"
                    sx={{
                      borderColor: '#e1dfdd',
                      color: '#605e5c',
                      textTransform: 'none',
                      fontWeight: 500,
                    }}
                  >
                    Add
                  </Button>
                </Box>
                <Box>
                  {formData.focusAreas.map((area) => (
                    <Chip
                      key={area}
                      label={area}
                      onDelete={() => removeFocusArea(area)}
                      sx={{ 
                        mr: 1, 
                        mb: 1,
                        backgroundColor: '#e3f2fd',
                        color: '#0078d4',
                        '& .MuiChip-deleteIcon': {
                          color: '#0078d4',
                        },
                      }}
                    />
                  ))}
                </Box>
              </Box>

              {/* Email Delivery Settings */}
              <Accordion sx={{ 
                border: '1px solid #e1dfdd',
                boxShadow: 'none',
                '&:before': { display: 'none' },
              }}>
                <AccordionSummary 
                  expandIcon={<ExpandMoreIcon />}
                  sx={{ backgroundColor: '#f3f2f1' }}
                >
                  <Box display="flex" alignItems="center">
                    <EmailIcon sx={{ mr: 2, color: '#0078d4' }} />
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        Email Delivery Settings
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Configure how and when reports are delivered
                      </Typography>
                    </Box>
                  </Box>
                </AccordionSummary>
                <AccordionDetails sx={{ backgroundColor: 'white' }}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={formData.enableEmailDelivery}
                          onChange={(e) => handleInputChange('enableEmailDelivery', e.target.checked)}
                          />
                        }
                        label="Enable Email Delivery"
                      />

                      {formData.enableEmailDelivery && (
                        <>
                          <TextField
                            fullWidth
                            type="email"
                            label="Your Email Address"
                            value={formData.userEmail}
                            onChange={(e) => handleInputChange('userEmail', e.target.value)}
                            required
                          />

                          <TextField
                            fullWidth
                            label="Your Name"
                            value={formData.userName}
                            onChange={(e) => handleInputChange('userName', e.target.value)}
                            placeholder="Research User"
                          />

                          <FormControl fullWidth>
                            <InputLabel>Delivery Format</InputLabel>
                            <Select
                              value={formData.deliveryFormat}
                              onChange={(e) => handleInputChange('deliveryFormat', e.target.value)}
                              label="Delivery Format"
                            >
                              {deliveryFormats.map((format) => (
                                <MenuItem key={format.value} value={format.value}>
                                  {format.label}
                                </MenuItem>
                              ))}
                            </Select>
                          </FormControl>

                          <FormControl fullWidth>
                            <InputLabel>Schedule</InputLabel>
                            <Select
                              value={formData.scheduleType}
                              onChange={(e) => handleInputChange('scheduleType', e.target.value)}
                              label="Schedule"
                            >
                              {scheduleTypes.map((schedule) => (
                                <MenuItem key={schedule.value} value={schedule.value}>
                                  {schedule.label}
                                </MenuItem>
                              ))}
                            </Select>
                          </FormControl>
                        </>
                      )}
                    </Box>
                  </AccordionDetails>
                </Accordion>                {/* Submit Button */}
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="large"
                  disabled={loading || !formData.query.trim() || (formData.enableEmailDelivery && !formData.userEmail.trim())}
                  startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                  sx={{ 
                    mt: 4,
                    py: 1.5,
                    textTransform: 'none',
                    fontWeight: 600,
                    backgroundColor: '#0078d4',
                    '&:hover': {
                      backgroundColor: '#005a9e',
                    },
                    '&:disabled': {
                      backgroundColor: '#d1d1d1',
                      color: '#666',
                    },
                  }}
                >
                  {loading ? 'Generating Report...' : 'Generate Research Report'}
                </Button>
                
                {/* Helper text for disabled button */}
                {(!formData.query.trim() || (formData.enableEmailDelivery && !formData.userEmail.trim())) && !loading && (
                  <Typography variant="caption" color="error" sx={{ mt: 1, display: 'block', textAlign: 'center' }}>
                    {!formData.query.trim() 
                      ? 'Please enter a research query' 
                      : 'Please enter your email address for delivery'}
                  </Typography>
                )}
              </Box>
            </Paper>
          </Grid>

        {/* Info Panel */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📊 Selected Agent
              </Typography>
              <Box display="flex" alignItems="center" mb={2}>
                {selectedAgent?.icon}
                <Typography variant="h6" sx={{ ml: 1 }}>
                  {selectedAgent?.label}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {selectedAgent?.description}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Results */}
        {(result || error) && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📋 Results
                </Typography>
                
                {error && (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                  </Alert>
                )}

                {result && (
                  <Box>
                    <Alert severity="success" sx={{ mb: 2 }}>
                      Research report generated successfully! 
                      {result.email_sent && ' Report has been sent to your email.'}
                    </Alert>
                    
                    <Typography variant="subtitle1" gutterBottom>
                      Report Details:
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Report ID: {result.report_id}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Request ID: {result.request_id}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Email Delivered: {result.email_sent ? 'Yes' : 'No'}
                    </Typography>
                    
                    {result.research_agent_output && (
                      <Accordion sx={{ mt: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                          <Typography>📊 Research Output</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                          <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                            <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                              {result.research_agent_output}
                            </Typography>
                          </Paper>
                        </AccordionDetails>
                      </Accordion>
                    )}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default EmailReportsManager;
