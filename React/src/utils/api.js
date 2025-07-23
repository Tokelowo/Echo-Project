const API_BASE_URL = "http://localhost:8000";

// API timeout configuration
const API_TIMEOUT = 30000; // 30 seconds timeout

export const fetchData = async (endpoint, options = {}) => {
  try {
    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    const defaultOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      mode: 'cors',
      signal: controller.signal, // Add abort signal
    };

    const mergedOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      }
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, mergedOptions);
    
    clearTimeout(timeoutId); // Clear timeout on successful response

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    // Clear timeout on any error
    if (typeof timeoutId !== 'undefined') clearTimeout(timeoutId);
    
    // Handle timeout specifically
    if (error.name === 'AbortError') {
      throw new Error(`Request timeout after ${API_TIMEOUT / 1000} seconds`);
    }
    
    // Don't log AbortError - it's expected behavior when components unmount
    if (error.name !== 'AbortError') {
      console.error(`Failed to fetch ${endpoint}:`, error);
    }
    throw error;
  }
};

export const fetchEnhancedMarketIntelligence = async (forceRefresh = false) => {
  try {
    const endpoint = `/api/enhanced-market-intelligence/?force_refresh=${forceRefresh}`;
    return await fetchData(endpoint);
  } catch (error) {
    throw error;
  }
};

export const fetchCompetitiveMetrics = async (forceRefresh = false) => {
  try {
    const endpoint = `/api/competitive-metrics/?force_refresh=${forceRefresh}`;
    return await fetchData(endpoint);
  } catch (error) {
    throw error;
  }
};

export const fetchMarketIntelligence = async () => {
  try {
    return await fetchData('/api/market-intelligence/');
  } catch (error) {
    throw error;
  }
};

export const fetchOverviewData = async (forceRefresh = false) => {
  try {
    const endpoint = `/api/overview/?force_refresh=${forceRefresh}`;
    return await fetchData(endpoint);
  } catch (error) {
    throw error;
  }
};

export const fetchCustomerReviews = async (forceRefresh = false) => {
  try {
    const endpoint = `/api/customer-reviews/?force_refresh=${forceRefresh}`;
    return await fetchData(endpoint);
  } catch (error) {
    throw error;
  }
};

// Fetch real market trends data (replaces hardcoded values)
export const fetchRealMarketTrendsData = async (forceRefresh = false) => {
  try {
    const params = forceRefresh ? '?force_refresh=true' : '';
    const response = await fetchData(`/api/real-market-trends-data/${params}`);
    
    if (response.error) {
      throw new Error(response.message || 'Failed to fetch real market trends data');
    }
    
    return response;
  } catch (error) {
    console.error('Error fetching real market trends data:', error);
    throw error;
  }
};

// Fetch enhanced product intelligence data with auto-updates
export const fetchEnhancedProductIntelligence = async (forceRefresh = false) => {
  try {
    const params = forceRefresh ? '?force_refresh=true' : '';
    const response = await fetchData(`/api/enhanced-product-intelligence/${params}`);
    
    if (response.error) {
      throw new Error(response.message || 'Failed to fetch enhanced product intelligence');
    }
    
    return response;
  } catch (error) {
    console.error('Error fetching enhanced product intelligence:', error);
    throw error;
  }
};

// Refresh product intelligence data manually
export const refreshProductIntelligence = async () => {
  try {
    const response = await fetchData('/api/refresh-product-intelligence/', {
      method: 'POST'
    });
    
    if (response.error) {
      throw new Error(response.message || 'Failed to refresh product intelligence');
    }
    
    return response;
  } catch (error) {
    console.error('Error refreshing product intelligence:', error);
    throw error;
  }
};

// Get product intelligence status
export const getProductIntelligenceStatus = async () => {
  try {
    const response = await fetchData('/api/product-intelligence-status/');
    
    if (response.error) {
      throw new Error(response.message || 'Failed to get product intelligence status');
    }
    
    return response;
  } catch (error) {
    console.error('Error getting product intelligence status:', error);
    throw error;
  }
};

export default API_BASE_URL;
