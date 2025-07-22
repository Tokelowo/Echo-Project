import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Button,
  Chip,
  LinearProgress,
  Paper,
  IconButton,
  Link,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import SecurityIcon from '@mui/icons-material/Security';
import ReportIcon from '@mui/icons-material/Report';
import RefreshIcon from '@mui/icons-material/Refresh';
import CloudIcon from '@mui/icons-material/Cloud';
import PsychologyIcon from '@mui/icons-material/Psychology';
import { Visibility, Launch, OpenInNew, Email as EmailIcon } from '@mui/icons-material';
import EmailSubscriptionDialog from '../components/EmailSubscriptionDialog';
import DataQualityIndicator from '../components/DataQualityIndicator';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const MetricCard = ({ title, value, subtitle, icon, color = 'primary', trend }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box>
          <Typography color="textSecondary" gutterBottom variant="h6">
            {title}
          </Typography>
          <Typography variant="h4" component="h2" color={color}>
            {value}
          </Typography>
          <Typography color="textSecondary" variant="body2">
            {subtitle}
          </Typography>
          {trend && (
            <Box sx={{ mt: 1 }}>
              <LinearProgress 
                variant="determinate" 
                value={trend} 
                sx={{ height: 8, borderRadius: 4 }}
                color={trend > 70 ? 'success' : trend > 40 ? 'warning' : 'error'}
              />
              <Typography variant="caption" color="textSecondary">
                Market Performance: {trend}%
              </Typography>
            </Box>
          )}
        </Box>
        <Box color={color}>{icon}</Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const navigate = useNavigate();
  const [overviewData, setOverviewData] = useState(null);
  const [agents, setAgents] = useState([]);
  const [reports, setReports] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [competitiveMetrics, setCompetitiveMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [subscriptionDialogOpen, setSubscriptionDialogOpen] = useState(false);
  const [sendingReport, setSendingReport] = useState(false);
  const [reportSent, setReportSent] = useState(false);
  const [emailDialogOpen, setEmailDialogOpen] = useState(false);
  const [emailData, setEmailData] = useState({ email: '', name: '' });

  // Function to fetch overview data from Django backend
  const fetchOverviewData = async (forceRefresh = false, signal = null) => {
    const baseUrl = 'http://127.0.0.1:8000/research-agent/overview/';
    const url = forceRefresh ? `${baseUrl}?force_refresh=true` : baseUrl;
    
    const fetchOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    };
    
    if (signal) {
      fetchOptions.signal = signal;
    }
    
    const response = await fetch(url, fetchOptions);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  };

  const fetchDashboardData = async (forceRefresh = false) => {
    if (forceRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }
    setError(null);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout
    
    try {
      const overviewResponse = await fetchOverviewData(forceRefresh, controller.signal);
      setOverviewData(overviewResponse);
      
      clearTimeout(timeoutId);
      
      setAgents(overviewResponse.agents_overview || []);
      setReports(overviewResponse.recent_reports || []);
      setMarketData(overviewResponse.market_intelligence || null);
      setCompetitiveMetrics(overviewResponse.competitive_intelligence || null);
      setLastUpdated(new Date(overviewResponse.last_updated));
    } catch (err) {
      clearTimeout(timeoutId);
      
      // Handle AbortError specifically - don't treat as a real error
      if (err.name === 'AbortError') {
        console.debug('Dashboard: Request was aborted (component unmounted or cleanup)');
        // Don't set error state for intentional aborts
        return;
      } else {
        console.error('Dashboard loading error:', err);
        setError(err.message);
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  const handleForceRefresh = () => {
    fetchDashboardData(true);
  };

  // Send one-time email report
  const sendOneTimeReport = async () => {
    if (!emailData.email) {
      alert('Please enter your email address');
      return;
    }
    
    setSendingReport(true);
    setEmailDialogOpen(false);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/research-agent/pipeline/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: 'Generate a comprehensive dashboard overview report with all current metrics and insights',
          agent_type: 'comprehensive_research',
          user_email: emailData.email,
          user_name: emailData.name || 'Dashboard Subscriber',
          delivery: {
            email: true,
            format: 'email'
          }
        }),
      });
      
      if (response.ok) {
        setReportSent(true);
        setEmailData({ email: '', name: '' }); // Reset form
        setTimeout(() => setReportSent(false), 5000); // Hide success message after 5 seconds
      } else {
        const errorText = await response.text();
        throw new Error(`Server responded with ${response.status}: ${errorText}`);
      }
    } catch (err) {
      console.error('Failed to send report:', err);
      alert(`Failed to send report: ${err.message}`);
    } finally {
      setSendingReport(false);
    }
  };

  useEffect(() => {
    let isMounted = true;
    
    const safeFetchData = async () => {
      if (isMounted) {
        try {
          await fetchDashboardData();
        } catch (err) {
          if (err.name !== 'AbortError') {
            console.error('Dashboard mount error:', err);
          }
        }
      }
    };
    
    safeFetchData();
    
    const refreshInterval = setInterval(() => {
      if (isMounted) {
        safeFetchData();
      }
    }, 15 * 60 * 1000); // 15 minutes
    
    return () => {
      isMounted = false;
      clearInterval(refreshInterval);
    };
  }, []);

  if (loading && agents.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  // Calculate metrics from overview data - use actual backend property names
  const activeAgents = overviewData?.agentsOnline || 0;
  const totalAgents = overviewData?.aiAgents || 0;
  const totalReports = overviewData?.threatReports || 0;
  const recentReports = overviewData?.threatReports || 0;

  // Market intelligence metrics from overview
  const microsoftArticles = overviewData?.totalReviews || 0;
  const competitorArticles = overviewData?.negativeReviews || 0;
  const marketTrendsCount = overviewData?.marketTrends?.length || 0;
  const threatIntelItems = overviewData?.activeThreats || 0;

  const marketTrendScore = microsoftArticles > 0 ? Math.min((microsoftArticles / Math.max(microsoftArticles + competitorArticles, 1)) * 100, 100) : 0;
  
  const competitiveData = overviewData?.cybersecurity || {};
  const marketPresenceData = overviewData?.marketTrends ? 
    overviewData.marketTrends.map((trend, index) => ({
      company: trend.name,
      articles: trend.score || 0,
      score: trend.score || 0,
      securityMentions: parseInt(trend.growth?.replace(/[^\d]/g, '')) || 0
    })) : [];
  
  const technologyTrendsData = overviewData?.marketTrends ? 
    overviewData.marketTrends.map((trend) => ({
      name: trend.name,
      value: trend.score || 0
    })) : [];

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1">
            🛡️ Real-Time Intelligence Dashboard
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            📡 Live cybersecurity threat intelligence • Last updated: {
              overviewData?.lastUpdated 
                ? new Date(overviewData.lastUpdated).toLocaleString()
                : new Date().toLocaleString()
            }
          </Typography>
          <Typography variant="caption" color="success.main">
            🔄 Auto-refreshes: 8 AM & 6 PM daily • Every 15 minutes
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={sendingReport ? <CircularProgress size={20} /> : <EmailIcon />}
            onClick={() => setEmailDialogOpen(true)}
            disabled={sendingReport}
            color="primary"
            size="small"
          >
            {sendingReport ? 'Generating Professional Report...' : 'Get Professional Report (.docx)'}
          </Button>
          <Button
            variant="outlined"
            startIcon={<EmailIcon />}
            onClick={() => setSubscriptionDialogOpen(true)}
            color="secondary"
            size="small"
          >
            Subscribe
          </Button>
          <Button
            variant="outlined"
            startIcon={refreshing ? <CircularProgress size={20} /> : <RefreshIcon />}
            onClick={handleForceRefresh}
            disabled={refreshing}
          >
            {refreshing ? 'Refreshing...' : 'Force Refresh'}
          </Button>
          <Button
            variant="outlined"
            startIcon={loading ? <CircularProgress size={20} /> : <RefreshIcon />}
            onClick={() => fetchDashboardData()}
            disabled={loading || refreshing}
          >
            {loading ? 'Loading...' : 'Refresh'}
          </Button>
        </Box>
      </Box>

      {/* Data Quality Indicator */}
      <DataQualityIndicator 
        dataType="mixed"
        lastUpdated={lastUpdated}
        sources={['Django Backend API', 'Live Intelligence Feeds', 'Market Data APIs']}
        confidence={overviewData ? 95 : 75}
        showDetails={true}
      />

      {(marketData?.last_updated || lastUpdated) && (        <Alert severity="info" sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', width: '100%' }}>
            <Box>
              <Typography variant="body1">
                Overview data last updated: {overviewData?.lastUpdated ? 
                  new Date(overviewData.lastUpdated).toLocaleString() : 
                  lastUpdated?.toLocaleString()}
              </Typography>
              <Typography variant="body2" sx={{ mt: 0.5, color: 'text.secondary' }}>
                📡 Auto-refresh: Every 30 minutes | 🌅 Daily refresh: 8:00 AM
              </Typography>
              <Typography variant="body2" sx={{ mt: 0.5 }}>
                🔗 Data Sources (Daily): {overviewData?.intelligence?.sources?.join(', ') || 'Django Backend API, Live Intelligence Feeds, Market Data APIs'}
              </Typography>
              <Typography variant="body2" sx={{ mt: 0.5 }}>
                🧠 Intelligence Mode: {overviewData?.intelligence?.mode || 'Enhanced'} - {overviewData?.intelligence?.status || 'Live Data'}
              </Typography>
            </Box><Box sx={{ display: 'flex', gap: 1 }}>
              <Chip 
                label="Enhanced Intelligence" 
                color="success"
                size="small"
              />
              <Chip 
                label="Live Data"
                color="secondary"
                size="small"
              />
            </Box>
          </Box>
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <Box>
            <Typography variant="h6">Connection Error</Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Error loading dashboard data: {error}
            </Typography>
            <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary' }}>
              Django Backend: http://127.0.0.1:8000/research-agent/overview/
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Check if the backend server is running and accessible.
            </Typography>
          </Box>
          <Button onClick={fetchDashboardData} sx={{ ml: 2 }}>
            Retry
          </Button>
        </Alert>
      )}

      {reportSent && (
        <Alert severity="success" sx={{ mb: 3 }}>
          📧 Dashboard report has been sent to your email! Check your inbox in a few minutes.
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Cybersecurity Intelligence Metrics */}
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Threat Reports"
            value={overviewData?.threatReports || 0}
            subtitle="Live cybersecurity intelligence"
            icon={<SecurityIcon />}
            color="error.main"
            trend={Math.min((overviewData?.threatReports || 0) * 2, 100)}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Threats"
            value={overviewData?.activeThreats || 0}
            subtitle={`Top: ${overviewData?.topThreat || 'Analyzing...'}`}
            icon={<ReportIcon />}
            color="warning.main"
            trend={overviewData?.activeThreats ? (overviewData.activeThreats * 8) : 0}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="AI Agents"
            value={`${activeAgents}/${totalAgents}`}
            subtitle="Research agents online"
            icon={<PsychologyIcon />}
            color="success.main"
            trend={totalAgents > 0 ? (activeAgents / totalAgents) * 100 : 0}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Attack Vector"
            value={overviewData?.attackVector || 'Email'}
            subtitle={`Primary attack method`}
            icon={<TrendingUpIcon />}
            color="info.main"
            trend={overviewData?.marketPerformance || 85}
          />
        </Grid>        {/* Market Presence Chart - Only show if we have data */}
        {marketPresenceData && marketPresenceData.length > 0 && (
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Real-Time Market Presence (News Coverage Analysis)
              </Typography>
              <Box sx={{ mb: 2, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  📊 Tracking vendor news coverage and market activity in today's cybersecurity headlines
                </Typography>
              </Box>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={marketPresenceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="company" angle={-20} textAnchor="end" height={60} />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => {
                      if (name === 'News Articles') return [`${value} articles`, 'Today\'s Coverage'];
                      if (name === 'Market Score') return [`${value}/100`, 'Market Activity Score'];
                      if (name === 'Security Mentions') return [`${value} mentions`, 'Security Features'];
                      return [value, name];
                    }}
                  />
                  <Legend />
                  <Bar dataKey="articles" fill="#8884d8" name="News Articles" />
                  <Bar dataKey="score" fill="#82ca9d" name="Market Score" />
                  <Bar dataKey="securityMentions" fill="#ffc658" name="Security Mentions" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}{/* Technology Trends - Only show if we have data */}
        {technologyTrendsData && technologyTrendsData.length > 0 && (
          <Grid item xs={12} md={6} lg={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                🔍 Technology Trends
              </Typography>
              <ResponsiveContainer width="100%" height={400}>
                <PieChart>
                  <Pie
                    data={technologyTrendsData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${value}%`}
                    outerRadius={100}
                    innerRadius={40}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {technologyTrendsData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value, name) => [`${value}%`, name]}
                    labelStyle={{ color: '#333', fontWeight: 'bold' }}
                  />
                  <Legend 
                    wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
                    iconType="circle"
                  />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>        )}

        {/* Live Threat Intelligence Summary */}
        {overviewData?.recent_reports && overviewData.recent_reports.length > 0 && (
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                🚨 Live Threat Intelligence
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                Real-time cybersecurity incidents and emerging threats
              </Typography>
              <Grid container spacing={2}>
                {overviewData.recent_reports.slice(0, 3).map((report, index) => (
                  <Grid item xs={12} md={4} key={report.id}>
                    <Card sx={{ height: '100%', borderLeft: `4px solid ${
                      report.priority === 'critical' ? '#f44336' : 
                      report.priority === 'high' ? '#ff9800' : '#4caf50'
                    }` }}>
                      <CardContent>
                        <Chip 
                          label={report.category.toUpperCase()} 
                          size="small" 
                          color={report.priority === 'critical' ? 'error' : 'warning'}
                          sx={{ mb: 1 }}
                        />
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                          {report.title.substring(0, 60)}...
                        </Typography>
                        <Typography variant="caption" color="textSecondary" display="block">
                          {report.agent_name} • {new Date(report.created_at).toLocaleTimeString()}
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1, fontSize: '0.875rem' }}>
                          {report.summary.substring(0, 100)}...
                        </Typography>
                        <Button 
                          size="small" 
                          href={report.url} 
                          target="_blank" 
                          sx={{ mt: 1 }}
                          endIcon={<OpenInNew />}
                        >
                          Details
                        </Button>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>
        )}

        {/* Threat Analytics Summary */}
        {overviewData?.trend_summary && (
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                📊 Threat Analytics
              </Typography>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="textSecondary">Most Active Threat</Typography>
                <Typography variant="h5" color="error.main" sx={{ fontWeight: 'bold' }}>
                  {overviewData.trend_summary.most_active_threat}
                </Typography>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="textSecondary">Trending Attack Vector</Typography>
                <Typography variant="h6" color="warning.main">
                  {overviewData.trend_summary.trending_attack_vector}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Total Threats Identified
                </Typography>
                <Typography variant="h4" color="info.main">
                  {overviewData.trend_summary.total_threats_identified}
                </Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="textSecondary">
                  Defense Technologies
                </Typography>
                <Typography variant="h6">
                  {overviewData.trend_summary.defense_technologies_mentioned || 0} Mentioned
                </Typography>
              </Box>
            </Paper>
          </Grid>
        )}

        {/* Recent Microsoft Developments - Only show if we have data */}
        {overviewData?.market_intelligence?.microsoft_news && 
         overviewData.market_intelligence.microsoft_news.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                <PsychologyIcon sx={{ mr: 1 }} />
                Latest Microsoft Developments
              </Typography>
              {overviewData.market_intelligence.microsoft_news.slice(0, 3).map((article, index) => (
                <Card key={index} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle2" color="primary">
                      {article.title}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {article.source} (Daily) - {new Date(article.published_date).toLocaleDateString()}
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {article.summary?.substring(0, 150)}...
                    </Typography>
                    <Button 
                      size="small" 
                      href={article.url} 
                      target="_blank" 
                      sx={{ mt: 1 }}
                    >
                      Read More
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </Paper>
          </Grid>
        )}

        {/* MDO Internal Capabilities - Only show if we have data */}
        {competitiveMetrics?.mdo_capabilities && Object.keys(competitiveMetrics.mdo_capabilities).length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <SecurityIcon sx={{ mr: 1 }} />
                MDO Internal Capabilities
              </Typography>
              <Box>
                {Object.entries(competitiveMetrics.mdo_capabilities).slice(0, 3).map(([feature, data], index) => (
                  <Box key={index} sx={{ mb: 2, p: 2, border: '1px solid #eee', borderRadius: 1 }}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      {feature.replace(/_/g, ' ').toUpperCase()}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      Latest Update: {data.latest_update || 'Q2 2025'}
                    </Typography>
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        Customer Satisfaction: {data.customer_satisfaction || 4.5}/5
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={(data.customer_satisfaction || 4.5) * 20} 
                        sx={{ mt: 0.5, height: 6, borderRadius: 3 }}
                        color="success"
                      />
                    </Box>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {(data.capabilities || []).slice(0, 3).map((capability, capIndex) => (
                        <Chip 
                          key={capIndex}
                          label={capability} 
                          size="small" 
                          variant="outlined"
                          color="primary"
                        />
                      ))}
                    </Box>                  </Box>
                ))}
                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                  🔒 Data from internal MDO knowledge base
                </Typography>
              </Box>
            </Paper>
          </Grid>
        )}        {/* Recent Cybersecurity Intelligence */}
        {overviewData?.recent_reports && overviewData.recent_reports.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Box>
                  <Typography variant="h6">
                    🛡️ Latest Cybersecurity Intelligence
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Real-time news from BleepingComputer, The Hacker News, Infosecurity Magazine, Dark Reading & more
                  </Typography>
                </Box>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<ReportIcon />}
                  onClick={() => navigate('/reports')}
                >
                  View All
                </Button>
              </Box>
              <Box>
                {overviewData.recent_reports.slice(0, 5).map((report) => (
                  <Box key={report.id} sx={{ mb: 2, pb: 2, borderBottom: '1px solid #eee' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Box sx={{ flex: 1 }}>                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <Chip
                            label={report.priority === 'critical' ? 'CRITICAL' : 
                                  report.priority === 'high' ? 'HIGH' : 'MEDIUM'}
                            color={report.priority === 'critical' ? 'error' : 
                                   report.priority === 'high' ? 'warning' : 'info'}
                            size="small"
                          />
                          <Chip
                            label={report.category === 'threat_protection' ? '🛡️ Threat Protection' :
                                   report.category === 'product_updates' ? '⚡ Product Updates' :
                                   report.category === 'threat_intelligence' ? '🔍 Threat Intel' :
                                   report.category === 'emerging_threats' ? '⚠️ Emerging Threats' :
                                   report.category === 'malware_analysis' ? '🦠 Malware' :
                                   report.category === 'security_updates' ? '🔒 Security Updates' :
                                   report.category === 'market_trends' ? '📈 Market Trends' : '📋 Compliance'}
                            variant="outlined"
                            size="small"
                          />
                          {report.relevance_score && (
                            <Chip
                              label={`${report.relevance_score.toFixed(1)}/10`}
                              color="success"
                              variant="outlined"
                              size="small"
                            />
                          )}
                        </Box>
                        <Link
                          href={report.url || '#'}
                          target={report.url ? '_blank' : '_self'}
                          rel={report.url ? 'noopener noreferrer' : undefined}
                          underline="hover"
                          sx={{ 
                            color: 'primary.main',
                            fontWeight: 600,
                            fontSize: '1rem',
                            display: 'block',
                            mb: 1
                          }}
                        >
                          {report.title}
                          {report.url && <OpenInNew sx={{ ml: 0.5, fontSize: '0.9rem' }} />}
                        </Link>
                        <Typography variant="body2" color="text.secondary" mb={1}>
                          {report.summary}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            📊 {report.agent_name} • {new Date(report.created_at).toLocaleDateString()}
                          </Typography>
                        </Box>
                      </Box>
                      <IconButton 
                        size="small" 
                        onClick={() => navigate('/reports')}
                        sx={{ ml: 1 }}
                        title="View detailed analysis"
                      >
                        <Visibility fontSize="small" />
                      </IconButton>
                    </Box>
                  </Box>
                ))}
                {overviewData.recent_reports.length > 5 && (
                  <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
                    +{overviewData.recent_reports.length - 5} more intelligence reports
                  </Typography>
                )}
              </Box>
            </Paper>
          </Grid>
        )}

        {/* Threat Intelligence Summary */}
        {competitiveMetrics?.threat_intelligence && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <SecurityIcon sx={{ mr: 1 }} />
                Threat Intelligence & Protection Effectiveness
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Latest Threats Detected
                  </Typography>
                  <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
                    {(competitiveMetrics.threat_intelligence.latest_threats || []).map((threat, index) => (
                      <Box key={index} sx={{ mb: 1, p: 1, backgroundColor: '#fff3e0', borderRadius: 1 }}>
                        <Typography variant="body2" color="primary">
                          {threat.threat_type || threat}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {threat.description || 'Advanced threat detected and mitigated'}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Protection Effectiveness
                  </Typography>
                  {Object.entries(competitiveMetrics.threat_intelligence.protection_effectiveness || {}).map(([metric, value], index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="body2">
                          {metric.replace(/_/g, ' ').toUpperCase()}
                        </Typography>
                        <Typography variant="body2" color="primary" fontWeight="bold">
                          {typeof value === 'number' ? `${value}%` : value}
                        </Typography>
                      </Box>
                      <LinearProgress 
                        variant="determinate" 
                        value={typeof value === 'number' ? value : 95} 
                        sx={{ mt: 0.5, height: 6, borderRadius: 3 }}
                        color={value > 90 ? 'success' : value > 70 ? 'warning' : 'error'}
                      />
                    </Box>
                  ))}
                </Grid>              </Grid>
            </Paper>
          </Grid>
        )}

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => navigate('/reports')}
                  startIcon={<ReportIcon />}
                >
                  View All Reports
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => navigate('/market')}
                  startIcon={<TrendingUpIcon />}
                >
                  Market Analysis
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => navigate('/competitors')}
                  startIcon={<AnalyticsIcon />}
                >
                  Competitor Research
                </Button>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => navigate('/intelligence')}
                  startIcon={<SecurityIcon />}
                >
                  Product Intelligence
                </Button>
              </Grid>            </Grid>
          </Paper>
        </Grid>

        {/* Data Sources Footer */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, backgroundColor: '#f8f9fa', border: '1px solid #e9ecef' }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
              <strong>📊 Live Data Sources (Updated Daily)</strong>
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Market Intelligence: RSS feeds, Industry reports, News aggregation (Daily refresh)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Competitive Analysis: Web scraping, Social media monitoring (Daily refresh)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Customer Analytics: MDO usage data, Performance metrics (Real-time)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1, fontStyle: 'italic' }}>
              Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })} | Data refreshed daily from live sources
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* One-Time Email Dialog */}
      <Dialog open={emailDialogOpen} onClose={() => setEmailDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <EmailIcon color="primary" />
            <Typography variant="h6">Send Dashboard Report</Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Get the latest Dashboard overview report with all current metrics and insights.
          </Typography>
          <TextField
            fullWidth
            label="Your Email"
            type="email"
            value={emailData.email}
            onChange={(e) => setEmailData(prev => ({ ...prev, email: e.target.value }))}
            required
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Your Name (Optional)"
            value={emailData.name}
            onChange={(e) => setEmailData(prev => ({ ...prev, name: e.target.value }))}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmailDialogOpen(false)}>
            Cancel
          </Button>
          <Button
            onClick={sendOneTimeReport}
            variant="contained"
            startIcon={<EmailIcon />}
            disabled={!emailData.email}
          >
            Send Report
          </Button>
        </DialogActions>
      </Dialog>

      {/* Email Subscription Dialog */}
      <EmailSubscriptionDialog
        open={subscriptionDialogOpen}
        onClose={() => setSubscriptionDialogOpen(false)}
        pageType="comprehensive_research"
      />
    </Box>
  );
};

export default Dashboard;
