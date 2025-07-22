import React, { useState, useEffect, lazy, Suspense } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Rating,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
  Button,
  Divider,
  Link,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Tooltip,
  IconButton
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  OpenInNew as OpenInNewIcon,
  TrendingUp,
  Assessment,
  Star,
  People,
  ThumbUp,
  Insights
} from '@mui/icons-material';
import { useAccessibility } from '../contexts/AccessibilityContext';
import { VendorOverviewChart, ReviewerSegmentChart } from './GartnerCharts';

// Lazy load the service only when needed
const loadGartnerService = () => import('../utils/gartnerReviewsService');

const GartnerReviewsIntegration = () => {
  const [reviewsData, setReviewsData] = useState(null);
  const [marketInsights, setMarketInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedVendor, setSelectedVendor] = useState(null);
  const { announce } = useAccessibility();

  useEffect(() => {
    loadGartnerData();
  }, []);

  const loadGartnerData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Dynamically load the service
      const { default: GartnerReviewsService } = await loadGartnerService();
      
      const [reviews, insights] = await Promise.all([
        GartnerReviewsService.fetchEmailSecurityReviews(),
        GartnerReviewsService.getMarketInsights()
      ]);
      
      setReviewsData(reviews);
      setMarketInsights(insights);
      announce('Gartner reviews data loaded successfully');
    } catch (err) {
      setError(err.message);
      announce('Failed to load Gartner reviews data');
    } finally {
      setLoading(false);
    }
  };

  const handleVendorSelect = (vendor) => {
    setSelectedVendor(vendor);
    announce(`Selected vendor: ${vendor.vendor_name}`);
  };

  const renderVendorOverview = () => {
    if (!reviewsData) return null;

    const chartData = reviewsData.vendors.map(vendor => ({
      name: vendor.vendor_name.replace(' for Office 365', '').replace(' Email', ''),
      rating: vendor.overall_rating,
      reviews: vendor.total_reviews,
      recommendation: vendor.recommendation_rate
    }));

    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Assessment color="primary" />
            Gartner Peer Insights - Email Security Platforms Overview
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Typography variant="subtitle2" gutterBottom>
                Vendor Ratings & Review Volume
              </Typography>
              <VendorOverviewChart data={chartData} />
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom>
                Market Summary
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Vendors Analyzed
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {reviewsData.total_vendors}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Reviews
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {reviewsData.total_reviews.toLocaleString()}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Market Size
                  </Typography>
                  <Typography variant="h6" color="primary">
                    ${marketInsights?.competitive_landscape?.market_size_usd || 'N/A'}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  const renderVendorComparison = () => {
    if (!reviewsData) return null;

    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <People color="primary" />
            Vendor Comparison Table
          </Typography>
          
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Vendor</strong></TableCell>
                  <TableCell align="center"><strong>Rating</strong></TableCell>
                  <TableCell align="center"><strong>Reviews</strong></TableCell>
                  <TableCell align="center"><strong>Recommendation Rate</strong></TableCell>
                  <TableCell align="center"><strong>Enterprise Focus</strong></TableCell>
                  <TableCell align="center"><strong>Actions</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {reviewsData.vendors.map((vendor, index) => (
                  <TableRow 
                    key={vendor.vendor_name}
                    sx={{ 
                      cursor: 'pointer',
                      '&:hover': { backgroundColor: 'action.hover' }
                    }}
                    onClick={() => handleVendorSelect(vendor)}
                  >
                    <TableCell>
                      <Typography variant="subtitle2">
                        {vendor.vendor_name}
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                        <Rating value={vendor.overall_rating} readOnly precision={0.1} size="small" />
                        <Typography variant="body2">
                          ({vendor.overall_rating})
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell align="center">
                      <Typography variant="body2">
                        {vendor.total_reviews.toLocaleString()}
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={vendor.recommendation_rate} 
                          sx={{ width: 60, height: 8 }}
                          color={vendor.recommendation_rate >= 85 ? 'success' : 'warning'}
                        />
                        <Typography variant="body2">
                          {vendor.recommendation_rate}%
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell align="center">
                      <Typography variant="body2">
                        {vendor.reviewer_segments?.['Enterprise (1000+ employees)'] || 0}%
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="View on Gartner Peer Insights">
                        <IconButton 
                          size="small"
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(vendor.gartner_peer_insights_url, '_blank');
                          }}
                        >
                          <OpenInNewIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    );
  };

  const renderVendorDetails = () => {
    if (!selectedVendor) return null;

    const segmentData = Object.entries(selectedVendor.reviewer_segments || {}).map(([segment, percentage]) => ({
      name: segment.replace(' (', '\\n('),
      value: percentage
    }));

    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Star color="primary" />
              {selectedVendor.vendor_name} - Detailed Analysis
            </Typography>
            <Button
              variant="outlined"
              size="small"
              onClick={() => setSelectedVendor(null)}
            >
              Close Details
            </Button>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom color="success.main">
                Key Strengths
              </Typography>
              <Box sx={{ mb: 2 }}>
                {selectedVendor.key_strengths?.map((strength, index) => (
                  <Chip
                    key={index}
                    label={strength}
                    size="small"
                    color="success"
                    variant="outlined"
                    sx={{ m: 0.5 }}
                  />
                ))}
              </Box>

              <Typography variant="subtitle2" gutterBottom color="warning.main">
                Key Weaknesses
              </Typography>
              <Box sx={{ mb: 2 }}>
                {selectedVendor.key_weaknesses?.map((weakness, index) => (
                  <Chip
                    key={index}
                    label={weakness}
                    size="small"
                    color="warning"
                    variant="outlined"
                    sx={{ m: 0.5 }}
                  />
                ))}
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Reviewer Segments
              </Typography>
              <ReviewerSegmentChart data={segmentData} />
            </Grid>
          </Grid>

          {selectedVendor.recent_reviews && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle2" gutterBottom>
                Recent Customer Reviews
              </Typography>
              {selectedVendor.recent_reviews.map((review, index) => (
                <Paper key={index} variant="outlined" sx={{ p: 2, mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Rating value={review.rating} readOnly size="small" />
                      <Typography variant="subtitle2">{review.title}</Typography>
                    </Box>
                    <Typography variant="caption" color="text.secondary">
                      {review.date}
                    </Typography>
                  </Box>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    "{review.review_snippet}"
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip label={review.reviewer_role} size="small" variant="outlined" />
                    <Chip label={review.company_size} size="small" variant="outlined" />
                  </Box>
                </Paper>
              ))}
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  const renderMarketInsights = () => {
    if (!marketInsights) return null;

    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Insights color="primary" />
            Gartner Market Insights & Trends
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom>
                Top Buying Factors
              </Typography>
              {marketInsights.market_insights.top_buying_factors.map((factor, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Typography variant="body2" sx={{ mr: 1 }}>
                    {index + 1}.
                  </Typography>
                  <Typography variant="body2">{factor}</Typography>
                </Box>
              ))}
            </Grid>

            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom>
                Emerging Trends
              </Typography>
              {marketInsights.market_insights.emerging_trends.map((trend, index) => (
                <Chip
                  key={index}
                  label={trend}
                  size="small"
                  color="primary"
                  variant="outlined"
                  sx={{ m: 0.25, display: 'block', mb: 1 }}
                />
              ))}
            </Grid>

            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" gutterBottom>
                Satisfaction Drivers
              </Typography>
              {marketInsights.market_insights.satisfaction_drivers.map((driver, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <ThumbUp sx={{ fontSize: 16, mr: 1, color: 'success.main' }} />
                  <Typography variant="body2">{driver}</Typography>
                </Box>
              ))}
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          <Typography variant="subtitle2" gutterBottom>
            Competitive Landscape
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Typography variant="body2" color="text.secondary">Market Leaders</Typography>
              {marketInsights.competitive_landscape.leaders.map((leader, index) => (
                <Chip key={index} label={leader} size="small" color="success" sx={{ m: 0.25 }} />
              ))}
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2" color="text.secondary">Challengers</Typography>
              {marketInsights.competitive_landscape.challengers.map((challenger, index) => (
                <Chip key={index} label={challenger} size="small" color="warning" sx={{ m: 0.25 }} />
              ))}
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2" color="text.secondary">Niche Players</Typography>
              {marketInsights.competitive_landscape.niche_players.map((niche, index) => (
                <Chip key={index} label={niche} size="small" color="info" sx={{ m: 0.25 }} />
              ))}
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2" color="text.secondary">Growth Rate</Typography>
              <Typography variant="h6" color="primary">
                {marketInsights.competitive_landscape.growth_rate}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Loading Gartner reviews data...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        <Typography variant="subtitle2">Failed to load Gartner reviews</Typography>
        <Typography variant="body2">{error}</Typography>
        <Button variant="contained" size="small" onClick={loadGartnerData} sx={{ mt: 1 }}>
          Retry
        </Button>
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Gartner Peer Insights Integration
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Competitive analysis and customer reviews from Gartner's Email Security Platforms market research
        </Typography>
      </Box>

      {renderVendorOverview()}
      {renderMarketInsights()}
      {renderVendorComparison()}
      {renderVendorDetails()}

      <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', border: 1, borderColor: 'divider', borderRadius: 1 }}>
        <Typography variant="caption" color="text.secondary">
          Data sourced from Gartner Peer Insights. Last updated: {reviewsData?.last_updated ? new Date(reviewsData.last_updated).toLocaleDateString() : 'N/A'}
          <br />
          <Link href="https://www.gartner.com/reviews/market/email-security-platforms" target="_blank" rel="noopener">
            View full Gartner Email Security Platforms reviews →
          </Link>
        </Typography>
      </Box>
    </Box>
  );
};

export default GartnerReviewsIntegration;
