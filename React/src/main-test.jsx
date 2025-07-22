import React from 'react';
import { createRoot } from 'react-dom/client';
import TestApp from './TestApp.jsx';
import './index.css';

console.log('main.jsx loaded');

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
console.log('Root element:', rootElement);

if (rootElement) {
  createRoot(rootElement).render(
    <React.StrictMode>
      <TestApp />
    </React.StrictMode>
  );
  console.log('React app mounted');
} else {
  console.error('Root element not found!');
}
