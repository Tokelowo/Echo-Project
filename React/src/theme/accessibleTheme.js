import { createTheme } from '@mui/material/styles';

// Enhanced accessible theme with improved contrast ratios and colors
export const createAccessibleTheme = (mode = 'light') => {
  const isLight = mode === 'light';
  
  return createTheme({
    palette: {
      mode,
      primary: {
        main: isLight ? '#0062cc' : '#4dabf7', // Improved contrast - WCAG AA compliant
        light: isLight ? '#4dabf7' : '#74c0fc',
        dark: isLight ? '#003d82' : '#1971c2',
        contrastText: '#ffffff',
      },
      secondary: {
        main: isLight ? '#0d7e0d' : '#51cf66', // Enhanced green with better contrast
        light: isLight ? '#51cf66' : '#8ce99a',
        dark: isLight ? '#0a5d0a' : '#37b24d',
        contrastText: '#ffffff',
      },
      error: {
        main: isLight ? '#d63384' : '#ff6b6b',
        light: isLight ? '#ff6b6b' : '#ffa8a8',
        dark: isLight ? '#b02a5b' : '#fa5252',
        contrastText: '#ffffff',
      },
      warning: {
        main: isLight ? '#fd7e14' : '#ffd43b',
        light: isLight ? '#ffd43b' : '#fff3bf',
        dark: isLight ? '#e8590c' : '#fab005',
        contrastText: isLight ? '#ffffff' : '#000000',
      },
      success: {
        main: isLight ? '#0d7e0d' : '#51cf66',
        light: isLight ? '#51cf66' : '#8ce99a',
        dark: isLight ? '#0a5d0a' : '#37b24d',
        contrastText: '#ffffff',
      },
      info: {
        main: isLight ? '#0062cc' : '#4dabf7',
        light: isLight ? '#4dabf7' : '#74c0fc',
        dark: isLight ? '#003d82' : '#1971c2',
        contrastText: '#ffffff',
      },
      background: {
        default: isLight ? '#fafafa' : '#121212',
        paper: isLight ? '#ffffff' : '#1e1e1e',
        // Custom accessibility backgrounds
        elevated: isLight ? '#f8f9fa' : '#2a2a2a',
        surface: isLight ? '#ffffff' : '#2d2d2d',
      },
      text: {
        primary: isLight ? '#212529' : '#ffffff', // Enhanced contrast
        secondary: isLight ? '#495057' : '#adb5bd', // Better secondary text contrast
        disabled: isLight ? '#868e96' : '#6c757d',
      },
      grey: {
        50: '#f8f9fa',
        100: '#f1f3f4',
        200: '#e9ecef',
        300: '#dee2e6',
        400: '#ced4da',
        500: '#adb5bd',
        600: '#6c757d',
        700: '#495057',
        800: '#343a40',
        900: '#212529',
      },
      // Custom accessibility colors
      focus: {
        main: isLight ? '#0066cc' : '#66b3ff',
        outline: isLight ? 'rgba(0, 102, 204, 0.4)' : 'rgba(102, 179, 255, 0.4)',
      },
      // High contrast mode colors
      highContrast: {
        text: isLight ? '#000000' : '#ffffff',
        background: isLight ? '#ffffff' : '#000000',
        border: isLight ? '#000000' : '#ffffff',
      },
    },
    typography: {
      fontFamily: '"Segoe UI", "Segoe UI Web", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif',
      // Enhanced font sizes for better readability
      h1: {
        fontSize: '2.75rem',
        fontWeight: 600,
        lineHeight: 1.2,
        letterSpacing: '-0.02em',
      },
      h2: {
        fontSize: '2.25rem',
        fontWeight: 600,
        lineHeight: 1.25,
        letterSpacing: '-0.01em',
      },
      h3: {
        fontSize: '1.875rem',
        fontWeight: 600,
        lineHeight: 1.3,
      },
      h4: {
        fontSize: '1.5rem',
        fontWeight: 600,
        lineHeight: 1.35,
      },
      h5: {
        fontSize: '1.25rem',
        fontWeight: 600,
        lineHeight: 1.4,
      },
      h6: {
        fontSize: '1.125rem',
        fontWeight: 600,
        lineHeight: 1.45,
      },
      body1: {
        fontSize: '1rem', // Increased from 0.875rem for better readability
        lineHeight: 1.6, // Improved line spacing
        letterSpacing: '0.00938em',
      },
      body2: {
        fontSize: '0.875rem', // Increased from 0.75rem
        lineHeight: 1.5,
        letterSpacing: '0.01071em',
      },
      button: {
        fontSize: '0.875rem',
        fontWeight: 600,
        lineHeight: 1.4,
        letterSpacing: '0.02857em',
        textTransform: 'none',
      },
      caption: {
        fontSize: '0.75rem',
        lineHeight: 1.4,
        letterSpacing: '0.03333em',
      },
      overline: {
        fontSize: '0.75rem',
        fontWeight: 600,
        lineHeight: 1.5,
        letterSpacing: '0.08333em',
        textTransform: 'uppercase',
      },
    },
    spacing: 8, // 8px base spacing unit
    shape: {
      borderRadius: 8, // Slightly larger for better touch targets
    },
    // Enhanced component styles with accessibility focus
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          '*': {
            boxSizing: 'border-box',
          },
          '*:focus-visible': {
            outline: `3px solid ${isLight ? '#0066cc' : '#66b3ff'}`,
            outlineOffset: '2px',
          },
          // Improve focus indicators
          'button:focus-visible, [role="button"]:focus-visible': {
            outline: `3px solid ${isLight ? '#0066cc' : '#66b3ff'}`,
            outlineOffset: '2px',
          },
          // Ensure minimum touch target size (44px)
          'button, [role="button"], input, select, textarea': {
            minHeight: '44px',
            minWidth: '44px',
          },
          // High contrast media query support
          '@media (prefers-contrast: high)': {
            '*': {
              borderColor: isLight ? '#000000' : '#ffffff',
            },
          },
          // Reduced motion support
          '@media (prefers-reduced-motion: reduce)': {
            '*': {
              animationDuration: '0.01ms !important',
              animationIterationCount: '1 !important',
              transitionDuration: '0.01ms !important',
            },
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            minHeight: '44px', // Accessibility minimum touch target
            padding: '12px 24px',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: 600,
            textTransform: 'none',
            '&:focus-visible': {
              outline: `3px solid ${isLight ? '#0066cc' : '#66b3ff'}`,
              outlineOffset: '2px',
            },
            '&:disabled': {
              opacity: 0.6,
              cursor: 'not-allowed',
            },
          },
          contained: {
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            '&:hover': {
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
              transform: 'translateY(-1px)',
            },
            '&:active': {
              transform: 'translateY(0)',
              boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
            },
          },
          outlined: {
            borderWidth: '2px',
            '&:hover': {
              borderWidth: '2px',
              backgroundColor: isLight ? 'rgba(0, 98, 204, 0.04)' : 'rgba(77, 171, 247, 0.08)',
            },
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: '12px',
            border: `1px solid ${isLight ? '#e9ecef' : '#343a40'}`,
            boxShadow: isLight 
              ? '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)'
              : '0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
            transition: 'all 0.2s ease-in-out',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: isLight
                ? '0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)'
                : '0 4px 6px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3)',
            },
          },
        },
      },
      MuiAppBar: {
        styleOverrides: {
          root: {
            backgroundColor: isLight ? '#ffffff' : '#1e1e1e',
            color: isLight ? '#212529' : '#ffffff',
            borderBottom: `1px solid ${isLight ? '#e9ecef' : '#343a40'}`,
            boxShadow: isLight
              ? '0 1px 3px rgba(0, 0, 0, 0.1)'
              : '0 1px 3px rgba(0, 0, 0, 0.3)',
          },
        },
      },
      MuiDrawer: {
        styleOverrides: {
          paper: {
            backgroundColor: isLight ? '#f8f9fa' : '#2a2a2a',
            borderRight: `1px solid ${isLight ? '#e9ecef' : '#343a40'}`,
          },
        },
      },
      MuiListItem: {
        styleOverrides: {
          root: {
            minHeight: '48px', // Better touch target
            borderRadius: '8px',
            margin: '4px 8px',
            '&:hover': {
              backgroundColor: isLight ? 'rgba(0, 98, 204, 0.08)' : 'rgba(77, 171, 247, 0.12)',
            },
            '&.Mui-selected': {
              backgroundColor: isLight ? 'rgba(0, 98, 204, 0.12)' : 'rgba(77, 171, 247, 0.16)',
              '&:hover': {
                backgroundColor: isLight ? 'rgba(0, 98, 204, 0.16)' : 'rgba(77, 171, 247, 0.20)',
              },
            },
          },
        },
      },
      MuiTextField: {
        styleOverrides: {
          root: {
            '& .MuiOutlinedInput-root': {
              borderRadius: '8px',
              '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: isLight ? '#0062cc' : '#4dabf7',
                borderWidth: '2px',
              },
              '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: isLight ? '#0062cc' : '#4dabf7',
                borderWidth: '2px',
              },
            },
          },
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            borderRadius: '16px',
            fontSize: '0.875rem',
            fontWeight: 500,
            '&:focus-visible': {
              outline: `3px solid ${isLight ? '#0066cc' : '#66b3ff'}`,
              outlineOffset: '2px',
            },
          },
        },
      },
      MuiAlert: {
        styleOverrides: {
          root: {
            borderRadius: '8px',
            fontSize: '0.875rem',
            '& .MuiAlert-icon': {
              fontSize: '1.25rem',
            },
          },
          standardSuccess: {
            backgroundColor: isLight ? '#d1e7dd' : '#2d5a41',
            color: isLight ? '#0a3622' : '#a3cfbb',
            border: `1px solid ${isLight ? '#0d7e0d' : '#51cf66'}`,
          },
          standardError: {
            backgroundColor: isLight ? '#f8d7da' : '#5a2a2d',
            color: isLight ? '#721c24' : '#f1959b',
            border: `1px solid ${isLight ? '#d63384' : '#ff6b6b'}`,
          },
          standardWarning: {
            backgroundColor: isLight ? '#fff3cd' : '#664d03',
            color: isLight ? '#664d03' : '#ffecb5',
            border: `1px solid ${isLight ? '#fd7e14' : '#ffd43b'}`,
          },
          standardInfo: {
            backgroundColor: isLight ? '#cff4fc' : '#055160',
            color: isLight ? '#055160' : '#b6effb',
            border: `1px solid ${isLight ? '#0062cc' : '#4dabf7'}`,
          },
        },
      },
      MuiTooltip: {
        styleOverrides: {
          tooltip: {
            backgroundColor: isLight ? '#343a40' : '#f8f9fa',
            color: isLight ? '#ffffff' : '#212529',
            fontSize: '0.875rem',
            borderRadius: '6px',
            padding: '8px 12px',
            maxWidth: '300px',
          },
          arrow: {
            color: isLight ? '#343a40' : '#f8f9fa',
          },
        },
      },
    },
    // Custom accessibility breakpoints
    breakpoints: {
      values: {
        xs: 0,
        sm: 600,
        md: 960,
        lg: 1280,
        xl: 1920,
      },
    },
  });
};
