import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Switch,
  FormControlLabel,
  Divider,
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Email as EmailIcon,
  Schedule as ScheduleIcon,
  Refresh as RefreshIcon,
  PlayArrow as ActivateIcon,
  Pause as PauseIcon,
  ExpandMore as ExpandMoreIcon,
  Settings as SettingsIcon,
  Unsubscribe as UnsubscribeIcon,
} from '@mui/icons-material';

const SubscriptionManager = () => {
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [editDialog, setEditDialog] = useState({ open: false, subscription: null });
  const [unsubscribeDialog, setUnsubscribeDialog] = useState({ open: false, subscription: null, all: false });

  const agentTypes = {
    'competitive_intelligence': 'Competitive Intelligence',
    'market_trends': 'Market Trends',
    'comprehensive_research': 'Comprehensive Multi-Agent Research',
    'strategic_action_summary': 'Strategic Action Summary',
    'customer_insights': 'Customer Insights'
  };

  const frequencies = {
    'daily': 'Daily',
    'weekly': 'Weekly',
    'monthly': 'Monthly'
  };

  const fetchSubscriptions = async () => {
    if (!userEmail.trim()) {
      setError('Please enter your email address');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`http://127.0.0.1:8000/manage-subscriptions/?email=${encodeURIComponent(userEmail)}`);
      const data = await response.json();
      
      if (data.success) {
        setSubscriptions(data.subscriptions);
        setSuccess(`Found ${data.total_subscriptions} subscription(s)`);
      } else {
        setError(data.error || 'Failed to fetch subscriptions');
      }
    } catch (err) {
      setError('Network error: Unable to fetch subscriptions');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateSubscription = async (subscriptionId, updates) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`http://127.0.0.1:8000/subscription/${subscriptionId}/update/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      });

      const data = await response.json();

      if (data.success) {
        setSuccess('Subscription updated successfully');
        await fetchSubscriptions();
        setEditDialog({ open: false, subscription: null });
      } else {
        setError(data.error || 'Failed to update subscription');
      }
    } catch (err) {
      setError('Network error: Unable to update subscription');
      console.error('Update error:', err);
    } finally {
      setLoading(false);
    }
  };

  const unsubscribeFromReport = async (subscriptionId) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`http://127.0.0.1:8000/subscription/${subscriptionId}/unsubscribe/`, {
        method: 'DELETE',
      });

      const data = await response.json();

      if (data.success) {
        setSuccess(data.message);
        await fetchSubscriptions();
        setUnsubscribeDialog({ open: false, subscription: null, all: false });
      } else {
        setError(data.error || 'Failed to unsubscribe');
      }
    } catch (err) {
      setError('Network error: Unable to unsubscribe');
      console.error('Unsubscribe error:', err);
    } finally {
      setLoading(false);
    }
  };

  const unsubscribeFromAll = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:8000/unsubscribe-all/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: userEmail }),
      });

      const data = await response.json();

      if (data.success) {
        setSuccess(data.message);
        await fetchSubscriptions();
        setUnsubscribeDialog({ open: false, subscription: null, all: false });
      } else {
        setError(data.error || 'Failed to unsubscribe from all');
      }
    } catch (err) {
      setError('Network error: Unable to unsubscribe from all');
      console.error('Unsubscribe all error:', err);
    } finally {
      setLoading(false);
    }
  };

  const reactivateSubscription = async (subscriptionId) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`http://127.0.0.1:8000/subscription/${subscriptionId}/reactivate/`, {
        method: 'POST',
      });

      const data = await response.json();

      if (data.success) {
        setSuccess(data.message);
        await fetchSubscriptions();
      } else {
        setError(data.error || 'Failed to reactivate subscription');
      }
    } catch (err) {
      setError('Network error: Unable to reactivate subscription');
      console.error('Reactivate error:', err);
    } finally {
      setLoading(false);
    }
  };

  const EditSubscriptionDialog = () => {
    const [editData, setEditData] = useState({});

    useEffect(() => {
      if (editDialog.subscription) {
        setEditData({
          frequency: editDialog.subscription.frequency,
          preferred_time: editDialog.subscription.preferred_time,
          time_zone: editDialog.subscription.time_zone,
          focus_areas: editDialog.subscription.focus_areas || [],
        });
      }
    }, [editDialog.subscription]);

    const handleSave = () => {
      updateSubscription(editDialog.subscription.id, editData);
    };

    return (
      <Dialog open={editDialog.open} onClose={() => setEditDialog({ open: false, subscription: null })} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <EditIcon />
            Edit Subscription
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {editDialog.subscription?.agent_type_display}
            </Typography>
            
            <FormControl fullWidth margin="normal">
              <InputLabel>Frequency</InputLabel>
              <Select
                value={editData.frequency || ''}
                label="Frequency"
                onChange={(e) => setEditData({ ...editData, frequency: e.target.value })}
              >
                <MenuItem value="daily">Daily</MenuItem>
                <MenuItem value="weekly">Weekly</MenuItem>
                <MenuItem value="monthly">Monthly</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              margin="normal"
              label="Preferred Time (HH:MM)"
              value={editData.preferred_time || ''}
              onChange={(e) => setEditData({ ...editData, preferred_time: e.target.value })}
              placeholder="09:00"
            />

            <TextField
              fullWidth
              margin="normal"
              label="Time Zone"
              value={editData.time_zone || ''}
              onChange={(e) => setEditData({ ...editData, time_zone: e.target.value })}
              placeholder="UTC"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialog({ open: false, subscription: null })}>
            Cancel
          </Button>
          <Button onClick={handleSave} variant="contained" disabled={loading}>
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>
    );
  };

  const UnsubscribeDialog = () => (
    <Dialog 
      open={unsubscribeDialog.open} 
      onClose={() => setUnsubscribeDialog({ open: false, subscription: null, all: false })}
    >
      <DialogTitle>
        <Box display="flex" alignItems="center" gap={1}>
          <UnsubscribeIcon />
          {unsubscribeDialog.all ? 'Unsubscribe from All' : 'Unsubscribe'}
        </Box>
      </DialogTitle>
      <DialogContent>
        <Typography>
          {unsubscribeDialog.all 
            ? `Are you sure you want to unsubscribe from all email reports for ${userEmail}?`
            : `Are you sure you want to unsubscribe from ${unsubscribeDialog.subscription?.agent_type_display} reports?`
          }
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          You can reactivate your subscription at any time.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setUnsubscribeDialog({ open: false, subscription: null, all: false })}>
          Cancel
        </Button>
        <Button 
          onClick={unsubscribeDialog.all ? unsubscribeFromAll : () => unsubscribeFromReport(unsubscribeDialog.subscription.id)}
          color="error" 
          variant="contained"
          disabled={loading}
        >
          Unsubscribe
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Card sx={{ maxWidth: 1000, mx: 'auto', my: 2 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SettingsIcon />
          Manage Email Subscriptions
        </Typography>

        {/* Email Input */}
        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            label="Your Email Address"
            value={userEmail}
            onChange={(e) => setUserEmail(e.target.value)}
            placeholder="Enter your email to manage subscriptions"
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            onClick={fetchSubscriptions}
            disabled={loading || !userEmail.trim()}
            startIcon={loading ? <CircularProgress size={20} /> : <RefreshIcon />}
          >
            {loading ? 'Loading...' : 'Load Subscriptions'}
          </Button>
        </Box>

        {/* Alerts */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
            {success}
          </Alert>
        )}

        {/* Subscriptions List */}
        {subscriptions.length > 0 && (
          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                Your Subscriptions ({subscriptions.filter(s => s.is_active).length} active)
              </Typography>
              <Button
                variant="outlined"
                color="error"
                startIcon={<UnsubscribeIcon />}
                onClick={() => setUnsubscribeDialog({ open: true, subscription: null, all: true })}
                disabled={subscriptions.filter(s => s.is_active).length === 0}
              >
                Unsubscribe from All
              </Button>
            </Box>

            <List>
              {subscriptions.map((subscription) => (
                <Paper key={subscription.id} sx={{ mb: 2 }}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="h6">
                            {subscription.agent_type_display}
                          </Typography>
                          <Chip
                            label={subscription.is_active ? 'Active' : 'Inactive'}
                            color={subscription.is_active ? 'success' : 'default'}
                            size="small"
                          />
                          <Chip
                            label={subscription.frequency_display}
                            variant="outlined"
                            size="small"
                          />
                        </Box>
                      }
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          <Typography variant="body2" color="text.secondary">
                            Next delivery: {subscription.next_delivery_local || 'Not scheduled'}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Preferred time: {subscription.preferred_time} ({subscription.time_zone})
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Reports sent: {subscription.total_reports_sent}
                          </Typography>
                        </Box>
                      }
                    />
                    <ListItemSecondaryAction>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        {subscription.is_active ? (
                          <>
                            <IconButton
                              edge="end"
                              onClick={() => setEditDialog({ open: true, subscription })}
                              title="Edit subscription"
                            >
                              <EditIcon />
                            </IconButton>
                            <IconButton
                              edge="end"
                              onClick={() => setUnsubscribeDialog({ open: true, subscription, all: false })}
                              title="Unsubscribe"
                              color="error"
                            >
                              <PauseIcon />
                            </IconButton>
                          </>
                        ) : (
                          <IconButton
                            edge="end"
                            onClick={() => reactivateSubscription(subscription.id)}
                            title="Reactivate subscription"
                            color="success"
                          >
                            <ActivateIcon />
                          </IconButton>
                        )}
                      </Box>
                    </ListItemSecondaryAction>
                  </ListItem>
                </Paper>
              ))}
            </List>
          </Box>
        )}

        {/* No Subscriptions Message */}
        {subscriptions.length === 0 && userEmail && !loading && (
          <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'grey.50' }}>
            <EmailIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              No subscriptions found
            </Typography>
            <Typography variant="body2" color="text.secondary">
              You don't have any email subscriptions for this email address.
            </Typography>
          </Paper>
        )}

        {/* Dialogs */}
        <EditSubscriptionDialog />
        <UnsubscribeDialog />
      </CardContent>
    </Card>
  );
};

export default SubscriptionManager;
