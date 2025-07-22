import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';

if (process.env.NODE_ENV === 'development') {
  const originalConsoleError = console.error;
  console.error = function(...args) {
    if (args[0] && typeof args[0] === 'string' && args[0].includes('validateDOMNesting')) {
      return;
    }
    originalConsoleError.apply(console, args);
  };
}

const rootElement = document.getElementById('root');
createRoot(rootElement).render(
  <App />
);
