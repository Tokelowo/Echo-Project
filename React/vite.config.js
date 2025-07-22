import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['react', 'react-dom', '@mui/material', '@mui/icons-material']
  },
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      input: {
        main: './index.html'
      },
      output: {
        manualChunks: {
          // Vendor chunks
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-mui': ['@mui/material', '@mui/icons-material', '@emotion/react', '@emotion/styled'],
          'vendor-charts': ['recharts'],
          
          // Feature chunks
          'dashboard': ['./src/pages/Dashboard.jsx', './src/components/layout/'],
          'competitor-analysis': ['./src/pages/CompetitorAnalysis.jsx', './src/components/GartnerReviewsIntegration.jsx'],
          'reports': ['./src/pages/Reports.jsx', './src/utils/reportExport.js'],
          'utils': ['./src/utils/api.js', './src/utils/newsApi.js', './src/utils/dateUtils.js']
        }
      }
    }
  },
  server: {
    port: 3000,
    strictPort: false,
    host: true,
    open: true,
    cors: true,
    proxy: {
      '/research-agent': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  preview: {
    port: 3000,
    strictPort: false,
    host: true
  },
  define: {
    'process.env.NODE_ENV': '"development"'
  },
  esbuild: {
    logOverride: { 'this-is-undefined-in-esm': 'silent' }
  }
});
