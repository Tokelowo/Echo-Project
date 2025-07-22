import React, { createContext, useContext, useState, useEffect } from 'react';

const AccessibilityContext = createContext();

export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider');
  }
  return context;
};

export const AccessibilityProvider = ({ children }) => {
  // Theme and display preferences
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  const [highContrast, setHighContrast] = useState(() => {
    const saved = localStorage.getItem('highContrast');
    return saved ? JSON.parse(saved) : window.matchMedia('(prefers-contrast: high)').matches;
  });

  const [reducedMotion, setReducedMotion] = useState(() => {
    const saved = localStorage.getItem('reducedMotion');
    return saved ? JSON.parse(saved) : window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  });

  // Font and text preferences
  const [fontSize, setFontSize] = useState(() => {
    const saved = localStorage.getItem('fontSize');
    return saved ? parseInt(saved) : 110; // percentage - increased default
  });

  const [dyslexiaFont, setDyslexiaFont] = useState(() => {
    const saved = localStorage.getItem('dyslexiaFont');
    return saved ? JSON.parse(saved) : false;
  });

  const [largeText, setLargeText] = useState(() => {
    const saved = localStorage.getItem('largeText');
    return saved ? JSON.parse(saved) : false;
  });

  // Screen reader and keyboard navigation
  const [screenReaderMode, setScreenReaderMode] = useState(() => {
    const saved = localStorage.getItem('screenReaderMode');
    return saved ? JSON.parse(saved) : false;
  });

  const [keyboardNavigation, setKeyboardNavigation] = useState(() => {
    const saved = localStorage.getItem('keyboardNavigation');
    return saved ? JSON.parse(saved) : false;
  });

  // Focus management
  const [focusVisible, setFocusVisible] = useState(false);
  const [announcements, setAnnouncements] = useState([]);
  const [speechEnabled, setSpeechEnabled] = useState(() => {
    const saved = localStorage.getItem('speechEnabled');
    return saved ? JSON.parse(saved) : false; // Default to OFF
  });

  // Auto-detect system preferences
  useEffect(() => {
    const mediaQueries = [
      { query: '(prefers-color-scheme: dark)', setState: setDarkMode },
      { query: '(prefers-contrast: high)', setState: setHighContrast },
      { query: '(prefers-reduced-motion: reduce)', setState: setReducedMotion },
    ];

    const listeners = mediaQueries.map(({ query, setState }) => {
      const mq = window.matchMedia(query);
      const listener = (e) => setState(e.matches);
      mq.addEventListener('change', listener);
      return { mq, listener };
    });

    return () => {
      listeners.forEach(({ mq, listener }) => {
        mq.removeEventListener('change', listener);
      });
    };
  }, []);

  // Persist preferences
  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem('highContrast', JSON.stringify(highContrast));
  }, [highContrast]);

  useEffect(() => {
    localStorage.setItem('reducedMotion', JSON.stringify(reducedMotion));
  }, [reducedMotion]);

  useEffect(() => {
    localStorage.setItem('fontSize', fontSize.toString());
  }, [fontSize]);

  useEffect(() => {
    localStorage.setItem('dyslexiaFont', JSON.stringify(dyslexiaFont));
  }, [dyslexiaFont]);

  useEffect(() => {
    localStorage.setItem('largeText', JSON.stringify(largeText));
  }, [largeText]);

  useEffect(() => {
    localStorage.setItem('screenReaderMode', JSON.stringify(screenReaderMode));
  }, [screenReaderMode]);

  useEffect(() => {
    localStorage.setItem('keyboardNavigation', JSON.stringify(keyboardNavigation));
  }, [keyboardNavigation]);

  useEffect(() => {
    localStorage.setItem('speechEnabled', JSON.stringify(speechEnabled));
  }, [speechEnabled]);

  // Apply CSS custom properties for accessibility
  useEffect(() => {
    const root = document.documentElement;
    
    // Font size scaling
    root.style.setProperty('--accessibility-font-scale', `${fontSize / 100}`);
    
    // Dyslexia-friendly font
    if (dyslexiaFont) {
      root.style.setProperty('--accessibility-font-family', '"OpenDyslexic", "Comic Sans MS", cursive');
    } else {
      root.style.setProperty('--accessibility-font-family', '"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif');
    }

    // High contrast mode
    if (highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }

    // Large text mode
    if (largeText) {
      root.classList.add('large-text');
    } else {
      root.classList.remove('large-text');
    }

    // Reduced motion
    if (reducedMotion) {
      root.classList.add('reduced-motion');
    } else {
      root.classList.remove('reduced-motion');
    }

    // Keyboard navigation mode
    if (keyboardNavigation) {
      root.classList.add('keyboard-navigation');
    } else {
      root.classList.remove('keyboard-navigation');
    }
  }, [fontSize, dyslexiaFont, highContrast, largeText, reducedMotion, keyboardNavigation]);

  // Keyboard navigation detection
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Tab') {
        setKeyboardNavigation(true);
      }
    };

    const handleMouseDown = () => {
      setKeyboardNavigation(false);
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('mousedown', handleMouseDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  // Screen reader announcements
  const announce = (message, priority = 'polite') => {
    const id = Date.now();
    setAnnouncements(prev => [...prev, { id, message, priority }]);
    
    // Only use browser speech synthesis if enabled
    if (speechEnabled && 'speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.rate = 0.8;
      utterance.volume = 0.7;
      utterance.pitch = 1;
      
      // Use a more natural voice if available
      const voices = speechSynthesis.getVoices();
      const englishVoice = voices.find(voice => voice.lang.startsWith('en-'));
      if (englishVoice) {
        utterance.voice = englishVoice;
      }
      
      speechSynthesis.speak(utterance);
    }
    
    // Remove announcement after it's been read
    setTimeout(() => {
      setAnnouncements(prev => prev.filter(a => a.id !== id));
    }, 3000); // Increased timeout for speech
  };

  // Stop all speech
  const stopSpeech = () => {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel();
    }
  };

  // Skip to content functionality
  const skipToContent = () => {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.focus();
      mainContent.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Focus management
  const trapFocus = (container) => {
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleKeyDown = (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
      if (e.key === 'Escape') {
        container.dispatchEvent(new CustomEvent('escape-focus-trap'));
      }
    };

    container.addEventListener('keydown', handleKeyDown);
    firstElement?.focus();

    return () => {
      container.removeEventListener('keydown', handleKeyDown);
    };
  };

  const value = {
    // State
    darkMode,
    highContrast,
    reducedMotion,
    fontSize,
    largeText,
    dyslexiaFont,
    screenReaderMode,
    keyboardNavigation,
    focusVisible,
    announcements,
    speechEnabled,

    // Actions
    setDarkMode,
    setHighContrast,
    setReducedMotion,
    setFontSize,
    setLargeText,
    setDyslexiaFont,
    setScreenReaderMode,
    setKeyboardNavigation,
    setSpeechEnabled,
    announce,
    stopSpeech,
    skipToContent,
    trapFocus,

    // Computed values
    isReducedMotion: reducedMotion,
    isHighContrast: highContrast,
    isDarkMode: darkMode,
    currentFontSize: fontSize,
  };

  return (
    <AccessibilityContext.Provider value={value}>
      {children}
      
      {/* Visual Announcement Debug Panel (for testing) */}
      {announcements.length > 0 && (
        <div
          style={{
            position: 'fixed',
            top: '20px',
            left: '20px',
            zIndex: 10000,
            background: 'rgba(0, 123, 255, 0.9)',
            color: 'white',
            padding: '12px 16px',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
            maxWidth: '300px',
            border: '2px solid #007bff',
            animation: 'pulse 1s infinite'
          }}
        >
          <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
            🔊 Screen Reader Announcement:
          </div>
          {announcements.map(a => (
            <div key={a.id} style={{ fontSize: '14px' }}>
              {a.message}
            </div>
          ))}
        </div>
      )}
      
      {/* Screen reader live region for announcements */}
      <div
        role="region"
        aria-live="polite"
        aria-label="Screen reader announcements"
        className="sr-only"
        style={{
          position: 'absolute',
          left: '-10000px',
          width: '1px',
          height: '1px',
          overflow: 'hidden',
        }}
      >
        {announcements
          .filter(a => a.priority === 'polite')
          .map(a => (
            <div key={a.id}>{a.message}</div>
          ))}
      </div>
      
      <div
        role="region"
        aria-live="assertive"
        aria-label="Urgent announcements"
        className="sr-only"
        style={{
          position: 'absolute',
          left: '-10000px',
          width: '1px',
          height: '1px',
          overflow: 'hidden',
        }}
      >
        {announcements
          .filter(a => a.priority === 'assertive')
          .map(a => (
            <div key={a.id}>{a.message}</div>
          ))}
      </div>
    </AccessibilityContext.Provider>
  );
};
