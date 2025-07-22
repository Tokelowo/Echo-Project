import React, { useState, useEffect, Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, CircularProgress, Box } from '@mui/material';
import { AccessibilityProvider, useAccessibility } from './contexts/AccessibilityContext';
import { createAccessibleTheme } from './theme/accessibleTheme';
import './styles/accessibility.css';
import Layout from './components/layout/Layout';
import ErrorBoundary from './components/ErrorBoundary';
import AccessibilityToolbar from './components/AccessibilityToolbar';

// Lazy load pages for code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const CompetitorAnalysis = lazy(() => import('./pages/CompetitorAnalysis'));
const ProductIntelligence = lazy(() => import('./pages/ProductIntelligence'));
const MarketTrends = lazy(() => import('./pages/MarketTrends'));
const Reports = lazy(() => import('./pages/Reports'));
const AccessibilityDemo = lazy(() => import('./pages/AccessibilityDemo'));
const SubscriptionManager = lazy(() => import('./components/SubscriptionManager'));

// Loading component
const LoadingSpinner = () => (
  <Box 
    sx={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '400px',
      flexDirection: 'column',
      gap: 2
    }}
  >
    <CircularProgress size={40} />
    <div>Loading...</div>
  </Box>
);

// Enhanced App component with accessibility
const AppContent = () => {
  const { darkMode, highContrast } = useAccessibility();
  const theme = createAccessibleTheme(darkMode ? 'dark' : 'light');

  // Apply high contrast styles when enabled
  useEffect(() => {
    const root = document.documentElement;
    if (highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
  }, [highContrast]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Alt + A to open accessibility menu
      if (e.altKey && e.key === 'a') {
        e.preventDefault();
        const accessibilityButton = document.querySelector('[aria-label="Open accessibility settings"]');
        if (accessibilityButton) {
          accessibilityButton.click();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/competitors" element={<CompetitorAnalysis />} />
              <Route path="/intelligence" element={<ProductIntelligence />} />
              <Route path="/market" element={<MarketTrends />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/subscriptions" element={<SubscriptionManager />} />
              <Route path="/accessibility" element={<AccessibilityDemo />} />
            </Routes>
          </Suspense>
        </Layout>
        <AccessibilityToolbar />
      </Router>
    </ThemeProvider>
  );
};

const App = () => {
  return (
    <ErrorBoundary>
      <AccessibilityProvider>
        <AppContent />
      </AccessibilityProvider>
    </ErrorBoundary>
  );
};
export default App;
