export const getTodayDate = () => {
  return new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

export const getTodayShort = () => {
  return new Date().toLocaleDateString();
};

export const getDailyUpdateLabel = () => {
  return `Last updated: ${getTodayDate()} | Data refreshed daily from live sources`;
};

export const getDailySourceLabel = (sourceType = 'data') => {
  return `${sourceType} refreshed daily`;
};

export const isDataFresh = (lastUpdate) => {
  if (!lastUpdate) return false;
  
  const lastUpdateDate = new Date(lastUpdate);
  const today = new Date();
  const diffTime = Math.abs(today - lastUpdateDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  return diffDays <= 1;
};

export const getDataFreshnessIndicator = (lastUpdate) => {
  const isFresh = isDataFresh(lastUpdate);
  return {
    status: isFresh ? 'fresh' : 'stale',
    color: isFresh ? 'success' : 'warning',
    label: isFresh ? 'Updated Today' : 'Update Pending'
  };
};
