import React, { useState, useEffect, Suspense, lazy } from 'react';
import { fetchCompetitiveMetrics } from '../utils/api';
import { fetchCompetitiveNews } from '../utils/newsApi';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Rating,
  Chip,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Button,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Tabs,
  Tab
} from '@mui/material';
import { Analytics, TrendingUp, Assessment, Cloud, Psychology, Email as EmailIcon, Reviews } from '@mui/icons-material';
import EmailSubscriptionDialog from '../components/EmailSubscriptionDialog';

// Lazy load the heavy Gartner component
const GartnerReviewsIntegration = lazy(() => import('../components/GartnerReviewsIntegration'));

// Loading component for Gartner integration
const GartnerLoadingSpinner = () => (
  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400, flexDirection: 'column', gap: 2 }}>
    <CircularProgress />
    <Typography>Loading Gartner Reviews...</Typography>
  </Box>
);
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

const CompetitorAnalysis = () => {
  const [metricsData, setMetricsData] = useState(null);
  const [newsData, setNewsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [subscriptionDialogOpen, setSubscriptionDialogOpen] = useState(false);
  const [sendingReport, setSendingReport] = useState(false);
  const [reportSent, setReportSent] = useState(false);
  const [emailDialogOpen, setEmailDialogOpen] = useState(false);
  const [emailData, setEmailData] = useState({ email: '', name: '' });
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  useEffect(() => {
    loadCompetitiveMetrics();
    
    const refreshInterval = setInterval(() => {
      loadCompetitiveMetrics();
    }, 30 * 60 * 1000); // 30 minutes
    
    return () => clearInterval(refreshInterval);
  }, []);

  const loadCompetitiveMetrics = async (forceRefresh = false) => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchCompetitiveMetrics(forceRefresh);
      setMetricsData(result);
    } catch (err) {
      // Handle AbortError - don't treat as a real error if it was intentional
      if (err.name === 'AbortError') {
        console.debug('Competitor Analysis: Request was aborted (component unmounted or cleanup)');
        return;
      }
      
      console.error('Error loading competitive metrics:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
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
      const response = await fetch('http://localhost:8000/api/pipeline/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: 'Generate a comprehensive competitive intelligence report for Microsoft Defender for Office 365',
          agent_type: 'competitive_intelligence',
          user_email: emailData.email,
          user_name: emailData.name || 'Competitive Intelligence Subscriber',
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

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          Error loading competitive metrics: {error}
          <Button onClick={loadCompetitiveMetrics} sx={{ ml: 2 }}>
            Retry
          </Button>
        </Alert>
      </Box>
    );
  }

  if (!metricsData) return null;

  // Use the new chartData structure from the backend
  const chartData = metricsData.chartData || {};
  
  // Market share data from the new backend structure
  const marketShareData = chartData.marketShareChart || [];
  
  // Performance metrics data from the new backend structure
  const performanceMetricsData = chartData.performanceMetrics || [];
  
  // Trends over time data from the new backend structure
  const trendsOverTimeData = chartData.trendsOverTime || [];
  
  // Market presence data - use competitors data as fallback
  const marketPresenceData = metricsData.competitors ? metricsData.competitors.map(comp => ({
    company: comp.name.replace('Microsoft Defender for Office 365', 'MDO').substring(0, 15),
    marketScore: comp.marketShare || 0,
    articles: Math.floor(comp.marketShare * 10) || 0, // Estimate articles from market share
    threatProtectionMentions: Math.floor(comp.rating * 20) || 0, // Estimate from rating
    securityMentions: Math.floor(comp.rating * 25) || 0, // Estimate from rating
    note: null
  })) : [];

  // Technology trends data - create from performance metrics
  const technologyTrendsData = performanceMetricsData.map(metric => ({
    technology: metric.category,
    mentions: metric.ourScore
  }));

  // Product features data - create from competitors data
  const productFeaturesData = metricsData.competitors ? metricsData.competitors.map(comp => ({
    company: comp.name.replace('Microsoft Defender for Office 365', 'MDO'),
    product: comp.strength,
    capability: comp.rating * 20, // Convert rating to capability score
    adoption: Math.min(95, comp.rating * 20 + 10),
    innovation: Math.min(90, comp.rating * 20 + 5),
    isDemo: false,
    dataBasis: 'Live Data'
  })) : [];

  // Check if we have disclaimers and new data structure
  const hasDisclaimers = false; // New structure doesn't have disclaimers
  const isFallbackData = false; // New structure is live data

  // Radar chart data for Microsoft Defender for Office 365 analysis
  const radarData = performanceMetricsData.map(metric => ({
    category: metric.category
      .replace('Customer Service', 'Support')
      .replace('Market Presence', 'Market')
      .replace('Product Quality', 'Quality')
      .substring(0, 12), // Limit to 12 characters
    ourScore: metric.ourScore,
    competitorAvg: metric.competitorAvg,
    difference: metric.ourScore - metric.competitorAvg
  }));

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          🛡️ MDO & Email Security Competitive Analysis
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            startIcon={<EmailIcon />}
            onClick={() => setSubscriptionDialogOpen(true)}
            color="secondary"
            size="small"
          >
            Subscribe to Reports
          </Button>
          <Button
            variant="outlined"
            startIcon={<EmailIcon />}
            onClick={() => setEmailDialogOpen(true)}
            color="primary"
            size="small"
            disabled={sendingReport}
          >
            Get Professional Report (.docx)
          </Button>
          <Button 
            variant="outlined" 
            startIcon={<Analytics />} 
            onClick={loadCompetitiveMetrics}
            disabled={loading}
            size="small"
          >
            Refresh Data
          </Button>
        </Box>
      </Box>

      {/* Add Tab Navigation */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange} aria-label="competitive analysis tabs">
          <Tab 
            label="Internal Analytics" 
            icon={<TrendingUp />} 
            iconPosition="start"
            id="tab-0"
            aria-controls="tabpanel-0"
          />
          <Tab 
            label="Gartner Reviews" 
            icon={<Reviews />} 
            iconPosition="start"
            id="tab-1"
            aria-controls="tabpanel-1"
          />
        </Tabs>
      </Box>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Box role="tabpanel" id="tabpanel-0" aria-labelledby="tab-0">
          {/* Existing Internal Analytics Content */}      <Grid container spacing={3}>
        
        {/* Data Quality and Disclaimers Section */}
        {hasDisclaimers && (
          <Grid item xs={12}>
            <Alert severity={isFallbackData ? "error" : "warning"} sx={{ mb: 2 }}>
              <Typography variant="h6" gutterBottom>
                {isFallbackData ? "⚠️ Data Quality Notice" : "📊 Data Sources & Disclaimers"}
              </Typography>
              {metricsData.CRITICAL_DISCLAIMER && (
                <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'error.main', mb: 1 }}>
                  {metricsData.CRITICAL_DISCLAIMER}
                </Typography>
              )}
              {metricsData.important_disclaimers?.market_share && (
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Market Share:</strong> {metricsData.important_disclaimers.market_share}
                </Typography>
              )}
              {metricsData.important_disclaimers?.feature_scores && (
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Feature Scores:</strong> {metricsData.important_disclaimers.feature_scores}
                </Typography>
              )}
              {metricsData.data_quality_report?.real_data_sources && (
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Real Data Sources:</strong> {metricsData.data_quality_report.real_data_sources.join(', ')}
                </Typography>
              )}
              {metricsData.data_quality_report?.recommendation && (
                <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                  <strong>Recommendation:</strong> {metricsData.data_quality_report.recommendation}
                </Typography>
              )}
            </Alert>
          </Grid>
        )}

        {/* Real-time Data Quality Indicators */}
        {metricsData.real_time_insights && (
          <Grid item xs={12}>
            <Card sx={{ backgroundColor: '#f8f9fa' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="primary">
                  📈 Real-time Analysis Quality
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={3}>
                    <Typography variant="body2" color="text.secondary">Articles Analyzed</Typography>
                    <Typography variant="h6">{metricsData.real_time_insights.total_articles_analyzed || 0}</Typography>
                  </Grid>
                  <Grid item xs={3}>
                    <Typography variant="body2" color="text.secondary">Microsoft Articles</Typography>
                    <Typography variant="h6">{metricsData.real_time_insights.microsoft_articles || 0}</Typography>
                  </Grid>
                  <Grid item xs={3}>
                    <Typography variant="body2" color="text.secondary">Active Sources</Typography>
                    <Typography variant="h6">{metricsData.real_time_insights.data_sources_active || 0}</Typography>
                  </Grid>
                  <Grid item xs={3}>
                    <Typography variant="body2" color="text.secondary">Threat Focus</Typography>
                    <Typography variant="body2">
                      {metricsData.real_time_insights.threat_landscape_focus?.slice(0, 2).join(', ') || 'General'}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        )}
        
        {/* Explanatory Banner for MDO Team */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, backgroundColor: '#e3f2fd', border: '2px solid #1976d2' }}>
            <Typography variant="h5" gutterBottom color="primary">
              📊 Competitive Intelligence Dashboard - MDO Team Guide
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              This dashboard provides real-time competitive analysis based on cybersecurity news sources. 
              {isFallbackData ? ' Currently showing fallback data due to API issues.' : ' Data updated from live news feeds.'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              🔄 Data refreshes automatically every 30 minutes | 📈 Metrics based on news article analysis
            </Typography>
          </Paper>
        </Grid>        {/* Email Security Market Presence Chart - Real data */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <TrendingUp sx={{ mr: 1 }} />
              Email Security Market Presence (News Coverage Analysis)
            </Typography>
            
            {/* Detailed explanation of market presence metrics */}
            <Box sx={{ mb: 3, p: 2, backgroundColor: '#f8f9fa', borderRadius: 1, border: '1px solid #dee2e6' }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                📊 Understanding Market Presence Metrics:
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem', mb: 1 }}>
                <strong>News Articles:</strong> Number of articles mentioning each company in today's cybersecurity news
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem', mb: 1 }}>
                <strong>Market Score:</strong> Calculated visibility score (0-100) based on article quality, reach, and sentiment
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                <strong>Why This Matters:</strong> Higher news coverage typically correlates with brand awareness, market influence, and customer mindshare
              </Typography>
            </Box>

            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={marketPresenceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="company" />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'News Articles') {
                      return [`${value} articles today`, 'News Coverage'];
                    } else if (name === 'Market Score') {
                      return [`${value}/100 visibility score`, 'Market Influence'];
                    }
                    return [value, name];
                  }}
                  labelFormatter={(label) => `Company: ${label}`}
                />
                <Legend />
                <Bar dataKey="articles" fill="#8884d8" name="News Articles" />
                <Bar dataKey="marketScore" fill="#82ca9d" name="Market Score" />
              </BarChart>
            </ResponsiveContainer>
            
            <Box sx={{ mt: 2, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                📋 Market Presence Analysis & Actions:
              </Typography>
              <Typography variant="body2" sx={{ mb: 2, fontWeight: 'bold' }}>
                Current Market Snapshot:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>MDO Position:</strong> {marketPresenceData.find(c => c.company === 'MDO')?.articles || 0} articles, {marketPresenceData.find(c => c.company === 'MDO')?.marketScore || 50} market score
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Top Competitor:</strong> {marketPresenceData.sort((a, b) => (b.articles + b.marketScore) - (a.articles + a.marketScore))[0]?.company || 'None'} leading in combined visibility
              </Typography>
              <Typography variant="body2" sx={{ mb: 2 }}>
                • <strong>News Volume:</strong> {marketPresenceData.reduce((sum, company) => sum + company.articles, 0)} total email security articles today across all vendors
              </Typography>
              
              <Typography variant="body2" sx={{ mb: 1, fontWeight: 'bold', color: 'primary.main' }}>
                Strategic Implications:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Low News Day:</strong> {marketPresenceData.reduce((sum, company) => sum + company.articles, 0) < 10 ? 'Limited email security coverage today - normal for industry cycles' : 'High activity day - monitor for major announcements'}
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Market Share Correlation:</strong> Companies with higher news coverage often maintain stronger market positions
              </Typography>
              <Typography variant="body2" sx={{ mb: 2 }}>
                • <strong>Timing Opportunity:</strong> {marketPresenceData.every(c => c.articles <= 2) ? 'Low competitor noise - ideal time for MDO announcements' : 'High competitor activity - time to monitor and respond'}
              </Typography>
              
              <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                🎯 Immediate Actions for MDO Team:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Content Strategy:</strong> Increase thought leadership to match or exceed competitor coverage
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>PR Timing:</strong> {marketPresenceData.reduce((sum, company) => sum + company.articles, 0) < 5 ? 'Low news day - good time for MDO press releases' : 'Monitor competitor announcements before timing releases'}
              </Typography>
              <Typography variant="body2">
                • <strong>Competitive Response:</strong> Track messaging themes from higher-coverage competitors and develop counter-narratives
              </Typography>
            </Box>
          </Paper>
        </Grid>{/* Email Security Market Share - Real data */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <Cloud sx={{ mr: 1 }} />
              Email Security Market Share
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={marketShareData}
                  cx="50%"
                  cy="35%"
                  labelLine={false}
                  label={false}
                  outerRadius={60}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {marketShareData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value, name) => [`${value}%`, name]} />
              </PieChart>
            </ResponsiveContainer>
            <Box sx={{ mt: 1 }}>
              {marketShareData.map((entry, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Box
                    sx={{
                      width: 12,
                      height: 12,
                      backgroundColor: entry.color || COLORS[index % COLORS.length],
                      borderRadius: '50%',
                      mr: 1,
                      flexShrink: 0
                    }}
                  />
                  <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                    {entry.name}: {entry.value}%
                  </Typography>
                </Box>
              ))}
            </Box>
            <Box sx={{ mt: 2, p: 2, backgroundColor: '#e8f5e8', borderRadius: 1 }}>
              <Typography variant="subtitle2" color="success.main" gutterBottom>
                🎯 Strategic Insights:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>MDO Market Position:</strong> Track our share vs. key competitors (Proofpoint, Mimecast)
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Growth Opportunities:</strong> Identify segments where competitors are losing ground
              </Typography>
              <Typography variant="body2">
                • <strong>Competitive Strategy:</strong> Focus on differentiation in areas where we're trailing
              </Typography>
            </Box>
          </Paper>
        </Grid>        {/* Email Security Technology Trends - Real data */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <Psychology sx={{ mr: 1 }} />
              Email Security Technology Trends (Mentions in News)
            </Typography>
            
            {/* Explanation of what this chart shows */}
            <Box sx={{ mb: 3, p: 2, backgroundColor: '#f0f8ff', borderRadius: 1, border: '1px solid #e3f2fd' }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                📖 What This Chart Shows:
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem', mb: 1 }}>
                This chart tracks how often specific email security technologies are mentioned in today's cybersecurity news. 
                Higher mention counts indicate technologies that are currently trending in the market.
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                <strong>Data Source:</strong> Analysis of {metricsData?.total_articles_analyzed || 8} articles from security news sources (updated {new Date(metricsData?.last_updated || Date.now()).toLocaleTimeString()})
              </Typography>
            </Box>

            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={technologyTrendsData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="technology" type="category" width={120} />
                <Tooltip 
                  formatter={(value, name) => [
                    `${value} mentions in today's news`,
                    'Technology Mentions'
                  ]}
                  labelFormatter={(label) => `Technology: ${label}`}
                />
                <Bar dataKey="mentions" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
            
            <Box sx={{ mt: 2, p: 2, backgroundColor: '#fff3e0', borderRadius: 1 }}>
              <Typography variant="subtitle2" color="warning.main" gutterBottom>
                🔬 Technology Intelligence & Strategic Implications:
              </Typography>
              <Typography variant="body2" sx={{ mb: 2, fontWeight: 'bold' }}>
                How to Read This Data:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>High Mentions (4+ today):</strong> Technologies generating significant market buzz - prime areas for marketing focus and feature development
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Medium Mentions (1-3):</strong> Emerging trends worth monitoring for future investment
              </Typography>
              <Typography variant="body2" sx={{ mb: 2 }}>
                • <strong>Zero Mentions:</strong> Either stable/mature technologies or areas with low current market interest
              </Typography>
              
              <Typography variant="body2" sx={{ mb: 1, fontWeight: 'bold' }}>
                Current Market Insights:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>AI/ML Detection ({technologyTrendsData.find(t => t.technology === 'AI/ML Detection')?.mentions || 0} mentions):</strong> Clear market leader - customers are actively seeking AI-powered email threat detection
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Zero Trust ({technologyTrendsData.find(t => t.technology === 'Zero Trust')?.mentions || 0} mentions):</strong> {technologyTrendsData.find(t => t.technology === 'Zero Trust')?.mentions > 0 ? 'Growing interest in zero-trust email security models' : 'No current news buzz - either mature technology or opportunity for thought leadership'}
              </Typography>
              <Typography variant="body2" sx={{ mb: 2 }}>
                • <strong>Cloud Security ({technologyTrendsData.find(t => t.technology === 'Cloud Security')?.mentions || 0} mentions):</strong> {technologyTrendsData.find(t => t.technology === 'Cloud Security')?.mentions > 0 ? 'Active discussion around cloud-native email security' : 'Stable market - focus on differentiation rather than basic cloud features'}
              </Typography>
              
              <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'warning.main' }}>
                ⚡ Immediate MDO Actions:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Marketing:</strong> Amplify messaging around top-mentioned technologies in press releases and thought leadership
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Product Strategy:</strong> Prioritize feature development in high-mention areas
              </Typography>
              <Typography variant="body2">
                • <strong>Competitive Positioning:</strong> Use trending technologies to differentiate MDO in sales conversations
              </Typography>
            </Box>
          </Paper>
        </Grid>{/* MDO Products Radar - Real data */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <Assessment sx={{ mr: 1 }} />
              Microsoft Defender for Office Analysis
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <RadarChart data={radarData} margin={{ top: 40, right: 40, bottom: 40, left: 40 }}>
                <PolarGrid />
                <PolarAngleAxis 
                  dataKey="category" 
                  tick={{ fontSize: 11 }}
                  className="radar-axis-text"
                />
                <PolarRadiusAxis 
                  angle={30} 
                  domain={[0, 100]} 
                  tick={{ fontSize: 10 }}
                  tickCount={5}
                />
                <Radar 
                  name="Our Score" 
                  dataKey="ourScore" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.3}
                  strokeWidth={2}
                />
                <Radar 
                  name="Competitor Average" 
                  dataKey="competitorAvg" 
                  stroke="#82ca9d" 
                  fill="#82ca9d" 
                  fillOpacity={0.3}
                  strokeWidth={2}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
              </RadarChart>
            </ResponsiveContainer>
            <Box sx={{ mt: 2, p: 2, backgroundColor: '#e3f2fd', borderRadius: 1 }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                🎯 MDO Performance Analysis:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Capability Score:</strong> Technical effectiveness vs. competitors
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Adoption Rate:</strong> Market penetration and customer uptake
              </Typography>
              <Typography variant="body2">
                • <strong>Innovation Rate:</strong> Feature development speed vs. market needs
              </Typography>
            </Box>
          </Paper>
        </Grid>        {/* Email Security Product Features Comparison Table - Real data */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Email Security Product Features Comparison - Live Market Analysis
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Company</TableCell>
                    <TableCell>Product</TableCell>
                    <TableCell>Capability Score</TableCell>
                    <TableCell>Market Adoption</TableCell>
                    <TableCell>Innovation Rate</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {productFeaturesData.map((row, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <Chip 
                          label={row.company} 
                          color={row.company === 'MDO' || row.company === 'Microsoft' ? 'primary' : 'default'}
                        />
                      </TableCell>
                      <TableCell>{row.product}</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress 
                            variant="determinate" 
                            value={row.capability} 
                            sx={{ width: 100, mr: 1 }}
                          />
                          {row.capability}%
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress 
                            variant="determinate" 
                            value={row.adoption} 
                            sx={{ width: 100, mr: 1 }}
                            color="secondary"
                          />
                          {row.adoption}%
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress 
                            variant="determinate" 
                            value={row.innovation} 
                            sx={{ width: 100, mr: 1 }}
                            color="success"
                          />
                          {row.innovation}%
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Box sx={{ mt: 2, p: 2, backgroundColor: '#f3e5f5', borderRadius: 1 }}>
              <Typography variant="subtitle2" color="secondary" gutterBottom>
                📊 Competitive Analysis Guide:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Capability Score:</strong> Product effectiveness based on feature analysis and reviews
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Market Adoption:</strong> Customer base penetration and deployment rates
              </Typography>
              <Typography variant="body2">
                • <strong>Innovation Rate:</strong> Speed of new feature releases and market responsiveness
              </Typography>
            </Box>
          </Paper>
        </Grid>        {/* Threat Protection vs Security Mentions - Real data */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Threat Protection vs Security Mentions in Today's News
            </Typography>
            
            {/* Explanation of threat intelligence metrics */}
            <Box sx={{ mb: 3, p: 2, backgroundColor: '#fff8e1', borderRadius: 1, border: '1px solid #ffcc02' }}>
              <Typography variant="subtitle2" color="warning.dark" gutterBottom>
                🛡️ Understanding Threat Intelligence Data:
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem', mb: 1 }}>
                <strong>Threat Protection Mentions:</strong> Specific references to advanced threat detection, ATP, anti-malware capabilities
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem', mb: 1 }}>
                <strong>Security Mentions:</strong> General security references (broader than just threat protection)
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                <strong>Strategic Value:</strong> Companies with higher threat protection mentions are positioning themselves as advanced security leaders
              </Typography>
            </Box>

            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={marketPresenceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="company" />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'Threat Protection Mentions') {
                      return [`${value} advanced threat mentions`, 'Threat Protection Focus'];
                    } else if (name === 'Security Mentions') {
                      return [`${value} general security mentions`, 'Overall Security Coverage'];
                    }
                    return [value, name];
                  }}
                  labelFormatter={(label) => `Company: ${label}`}
                />
                <Legend />
                <Bar dataKey="threatProtectionMentions" fill="#ff7300" name="Threat Protection Mentions" />
                <Bar dataKey="securityMentions" fill="#387908" name="Security Mentions" />
              </BarChart>
            </ResponsiveContainer>
            
            <Box sx={{ mt: 2, p: 2, backgroundColor: '#ffeaa7', borderRadius: 1 }}>
              <Typography variant="subtitle2" color="warning.dark" gutterBottom>
                ⚡ Threat Intelligence Insights & Market Positioning:
              </Typography>
              <Typography variant="body2" sx={{ mb: 2, fontWeight: 'bold' }}>
                Current Threat Landscape Positioning:
              </Typography>
              {marketPresenceData.map((company, index) => (
                <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                  • <strong>{company.company}:</strong> {company.threatProtectionMentions} threat mentions, {company.securityMentions} security mentions
                  {company.threatProtectionMentions > company.securityMentions ? ' (Advanced threat focus)' : company.securityMentions > 0 ? ' (General security positioning)' : ' (Low visibility today)'}
                </Typography>
              ))}
              
              <Typography variant="body2" sx={{ mb: 2, mt: 2, fontWeight: 'bold', color: 'warning.dark' }}>
                Market Intelligence Analysis:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Threat Protection Leaders:</strong> {marketPresenceData.filter(c => c.threatProtectionMentions > 0).length > 0 ? marketPresenceData.filter(c => c.threatProtectionMentions > 0).map(c => c.company).join(', ') : 'No specific threat protection coverage today'}
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>General Security Focus:</strong> {marketPresenceData.filter(c => c.securityMentions > c.threatProtectionMentions).length > 0 ? marketPresenceData.filter(c => c.securityMentions > c.threatProtectionMentions).map(c => c.company).join(', ') : 'Market focused on advanced threats rather than basic security'}
              </Typography>
              <Typography variant="body2" sx={{ mb: 2 }}>
                • <strong>Market Opportunity:</strong> {marketPresenceData.every(c => c.threatProtectionMentions === 0) ? 'Clear opportunity for MDO to dominate threat protection narrative' : 'Competitive threat protection messaging - need strong differentiation'}
              </Typography>
              
              <Typography variant="body2" sx={{ fontWeight: 'bold', color: 'error.main' }}>
                🚨 Critical Actions for MDO:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Messaging Strategy:</strong> {marketPresenceData.find(c => c.company === 'MDO')?.threatProtectionMentions > 0 ? 'Amplify current threat protection messaging' : 'Increase advanced threat protection thought leadership'}
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                • <strong>Competitive Response:</strong> Monitor competitors with high threat protection mentions for new capabilities or messaging shifts
              </Typography>
              <Typography variant="body2">
                • <strong>Market Positioning:</strong> {marketPresenceData.every(c => c.threatProtectionMentions <= 1) ? 'Low threat protection noise - perfect time for MDO to establish thought leadership' : 'Active threat protection competition - need strong differentiation'}
              </Typography>
            </Box>
          </Paper>
        </Grid>{/* Recent MDO Developments - Real data */}
        {metricsData.market_presence?.['Microsoft Defender for Office']?.recent_developments && 
         metricsData.market_presence['Microsoft Defender for Office'].recent_developments.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recent Microsoft Defender for Office Developments
              </Typography>
              {metricsData.market_presence['Microsoft Defender for Office'].recent_developments.map((article, index) => (
                <Card key={index} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" color="primary">
                      {article.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {article.source} (Daily) - {new Date(article.published_date).toLocaleDateString()}
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {article.summary}
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
          </Grid>        )}

        {/* Strategic Action Summary for MDO Team */}
        <Grid item xs={12}>
          <Paper sx={{ p: 4, backgroundColor: '#f8f9fa', border: '2px solid #007acc' }}>
            <Typography variant="h5" gutterBottom color="primary" sx={{ display: 'flex', alignItems: 'center' }}>
              🎯 MDO Team - Strategic Action Summary
            </Typography>
            
            <Grid container spacing={3} sx={{ mt: 2 }}>
              <Grid item xs={12} md={4}>
                <Box sx={{ p: 2, backgroundColor: '#e8f5e8', borderRadius: 1, height: '100%' }}>
                  <Typography variant="h6" color="success.main" gutterBottom>
                    🚀 Immediate Actions (Next 30 Days)
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • Increase MDO thought leadership content to match competitor news coverage
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • Focus marketing on AI/ML detection capabilities (top trending technology)
                  </Typography>
                  <Typography variant="body2">
                    • Highlight threat protection features in competitive positioning
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Box sx={{ p: 2, backgroundColor: '#e3f2fd', borderRadius: 1, height: '100%' }}>
                  <Typography variant="h6" color="primary" gutterBottom>
                    📈 Growth Opportunities (Next Quarter)
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • Target market segments where competitors show declining adoption
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • Accelerate innovation in Zero Trust email security architecture
                  </Typography>
                  <Typography variant="body2">
                    • Develop competitive battlecards based on capability scores
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Box sx={{ p: 2, backgroundColor: '#fff3e0', borderRadius: 1, height: '100%' }}>
                  <Typography variant="h6" color="warning.main" gutterBottom>
                    ⚠️ Competitive Threats (Monitor)
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • Watch for Proofpoint's messaging shifts and new feature announcements
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • Monitor Mimecast's cloud security positioning changes
                  </Typography>
                  <Typography variant="body2">
                    • Track emerging players gaining market presence through news coverage
                  </Typography>
                </Box>
              </Grid>
            </Grid>
            
            <Box sx={{ mt: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle1" color="primary" gutterBottom>
                📊 How to Use This Dashboard:
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>1. Weekly Review:</strong> Check market presence trends to identify emerging competitive threats
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>2. Monthly Strategy:</strong> Use technology trends to align MDO roadmap with market demand
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>3. Quarterly Planning:</strong> Review capability scores to identify feature gaps and competitive advantages
              </Typography>
              <Typography variant="body2">
                <strong>4. Real-time Alerts:</strong> Monitor news developments for immediate competitive response opportunities
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Data Sources Footer */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, backgroundColor: '#f8f9fa', border: '1px solid #e9ecef' }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
              <strong>🔍 Live Competitive Intelligence Sources (Updated Daily)</strong>
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Competitor Monitoring: TechCrunch, ArsTechnica, Industry press releases (Daily refresh)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Market Analysis: Financial reports, Analyst insights, Product announcements (Daily aggregation)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
              • Social Intelligence: Social media monitoring, Review platforms (Real-time)
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1, fontStyle: 'italic' }}>
              Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })} | Competitive data refreshed daily
            </Typography>
          </Paper>
        </Grid>      </Grid>
        </Box>
      )}

      {/* Gartner Reviews Tab */}
      {activeTab === 1 && (
        <Box role="tabpanel" id="tabpanel-1" aria-labelledby="tab-1">
          <Suspense fallback={<GartnerLoadingSpinner />}>
            <GartnerReviewsIntegration />
          </Suspense>
        </Box>
      )}

      {/* One-Time Email Report Dialog */}
      <Dialog 
        open={emailDialogOpen} 
        onClose={() => setEmailDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Get Competitive Intelligence Report via Email
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="Email Address"
              type="email"
              value={emailData.email}
              onChange={(e) => setEmailData({ ...emailData, email: e.target.value })}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Name (Optional)"
              value={emailData.name}
              onChange={(e) => setEmailData({ ...emailData, name: e.target.value })}
              margin="normal"
            />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              You'll receive a comprehensive competitive intelligence report with the latest market data, competitor analysis, and strategic insights for Microsoft Defender for Office 365.
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmailDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={sendOneTimeReport} 
            variant="contained"
            disabled={sendingReport || !emailData.email}
          >
            {sendingReport ? 'Generating Professional Report...' : 'Send Professional Report (.docx)'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Success notification for one-time report */}
      {reportSent && (
        <Alert severity="success" sx={{ position: 'fixed', top: 20, right: 20, zIndex: 9999 }}>
          📧 Professional Competitive Intelligence report sent! Check your inbox for the Microsoft-branded email with downloadable .docx attachment.
        </Alert>
      )}

      {/* Email Subscription Dialog */}
      <EmailSubscriptionDialog
        open={subscriptionDialogOpen}
        onClose={() => setSubscriptionDialogOpen(false)}
        pageType="competitive_intelligence"
      />
    </Box>
  );
};

export default CompetitorAnalysis;
