import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { 
  Description, 
  Refresh, 
  Visibility, 
  Download, 
  Add,
  Assessment,
  TrendingUp,
  Security
} from '@mui/icons-material';
import { fetchData } from '../utils/api';
import { fetchResearchAgentData } from '../utils/reportExport';

const ReportCard = ({ report, onView }) => {
  const getReportIcon = (title) => {
    if (title.toLowerCase().includes('market')) return <TrendingUp color="primary" />;
    if (title.toLowerCase().includes('competitor')) return <Assessment color="success" />;
    if (title.toLowerCase().includes('security')) return <Security color="error" />;
    return <Description color="info" />;
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box sx={{ flex: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              {getReportIcon(report.title)}
              <Typography variant="h6" sx={{ ml: 1 }}>
                {report.title}
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Agent: {report.agent?.name || 'Unknown'}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Created: {new Date(report.created_at || report.timestamp).toLocaleDateString()}
            </Typography>            <Typography variant="body2" paragraph>
              {(report.content) ? 
                // Clean preview text
                report.content
                  .replace(/#{1,6}\s/g, '') // Remove markdown headers
                  .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold markdown
                  .replace(/\*(.*?)\*/g, '$1') // Remove italic markdown
                  .replace(/<[^>]*>/g, '') // Remove HTML tags
                  .replace(/---+/g, '') // Remove horizontal rules
                  .trim()
                  .substring(0, 150) + '...' : 
                'Content loading...'}
            </Typography>
          </Box>
          <Box sx={{ ml: 2 }}>
            <IconButton onClick={() => onView(report)} color="primary">
              <Visibility />
            </IconButton>
            <IconButton color="primary">
              <Download />
            </IconButton>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReport, setSelectedReport] = useState(null);
  const [generating, setGenerating] = useState(false);

  const fetchReports = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await fetchData('/reports/');
      setReports(data.results || data || []);
    } catch (err) {
      // Handle AbortError - don't treat as a real error if it was intentional
      if (err.name === 'AbortError') {
        console.debug('Reports: Request was aborted (component unmounted or cleanup)');
        return;
      }
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const generateNewReport = async () => {
    setGenerating(true);
    setError(null);
    
    try {
      const result = await fetchResearchAgentData('/comprehensive-research/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: 'Generate comprehensive research report covering market trends, competitive analysis, and product intelligence',
          focus_areas: ['Market Analysis', 'Competitive Intelligence', 'Product Strategy'],
          user_name: 'Report Generator',
        }),
      });
      
      // Refresh reports list after generation
      await fetchReports();
      
      alert('New report generated successfully!');
    } catch (err) {
      // Handle AbortError - don't treat as a real error if it was intentional
      if (err.name === 'AbortError') {
        console.debug('Reports: Generate request was aborted (component unmounted or cleanup)');
        return;
      }
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleViewReport = (report) => {
    setSelectedReport(report);
  };

  const handleCloseDialog = () => {
    setSelectedReport(null);
  };

  if (loading && reports.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Reports
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={loading ? <CircularProgress size={20} /> : <Refresh />}
            onClick={fetchReports}
            disabled={loading}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={generating ? <CircularProgress size={20} /> : <Add />}
            onClick={generateNewReport}
            disabled={generating}
          >
            {generating ? 'Generating...' : 'Generate Report'}
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error: {error}
          <Button onClick={fetchReports} sx={{ ml: 2 }}>
            Retry
          </Button>
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Reports Statistics */}
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Report Statistics
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="h4" color="primary">
                {reports.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Reports
              </Typography>
            </Box>
            <Box sx={{ mb: 2 }}>
              <Typography variant="h4" color="success.main">
                {reports.filter(r => {
                  const date = new Date(r.created_at || r.timestamp);
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return date > weekAgo;
                }).length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This Week
              </Typography>
            </Box>
            <Box>
              <Typography variant="h4" color="info.main">
                {new Set(reports.map(r => r.agent?.name || 'Unknown')).size}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Active Agents
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Reports List */}
        <Grid item xs={12} md={9}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Generated Reports
            </Typography>
            
            {reports.length > 0 ? (
              <Box>
                {reports.map((report) => (
                  <ReportCard 
                    key={report.id} 
                    report={report} 
                    onView={handleViewReport}
                  />
                ))}
              </Box>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="body1" color="text.secondary" gutterBottom>
                  No reports found. Generate your first report to get started.
                </Typography>
                <Button 
                  variant="contained" 
                  onClick={generateNewReport}
                  startIcon={<Add />}
                  disabled={generating}
                >
                  {generating ? 'Generating...' : 'Generate First Report'}
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Report Title</TableCell>
                    <TableCell>Agent</TableCell>
                    <TableCell>Created</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {reports.slice(0, 5).map((report) => (
                    <TableRow key={report.id}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Description sx={{ mr: 1 }} />
                          {report.title}
                        </Box>
                      </TableCell>
                      <TableCell>{report.agent?.name || 'Unknown'}</TableCell>
                      <TableCell>
                        {new Date(report.created_at || report.timestamp).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <Chip label="Complete" color="success" size="small" />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" onClick={() => handleViewReport(report)}>
                          <Visibility />
                        </IconButton>
                        <IconButton size="small">
                          <Download />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>          </Paper>
        </Grid>

        {/* Data Sources Footer */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, backgroundColor: '#f8f9fa', border: '1px solid #e9ecef' }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
              <strong>📋 Report Data Sources (Updated Daily)</strong>
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Market Reports: Industry analysis, Financial data, Trend research (Daily refresh)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Competitive Intelligence: News aggregation, Company analysis, Product updates (Daily refresh)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Security Analysis: Threat intelligence, Vulnerability data, Industry insights (Real-time)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1, fontStyle: 'italic' }}>
              Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })} | Reports generated daily from live sources
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Report View Dialog */}
      <Dialog 
        open={!!selectedReport}
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedReport?.title}
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Agent: {selectedReport?.agent?.name || 'Unknown'} | 
            Created: {selectedReport ? new Date(selectedReport.created_at || selectedReport.timestamp).toLocaleDateString() : ''}
          </Typography>          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', mt: 2 }}>
            {selectedReport?.content ? 
              // Remove HTML tags and convert markdown-style formatting for better display
              selectedReport.content
                .replace(/#{1,6}\s/g, '') // Remove markdown headers
                .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold markdown
                .replace(/\*(.*?)\*/g, '$1') // Remove italic markdown
                .replace(/<[^>]*>/g, '') // Remove HTML tags
                .replace(/---+/g, '') // Remove horizontal rules
                .trim()
              : 'Loading content...'}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Close</Button>
          <Button variant="contained" startIcon={<Download />}>
            Download
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Reports;
