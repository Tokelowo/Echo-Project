import React from 'react';

const TestApp = () => {
  return (
    <div style={{ padding: '20px', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
      <h1>React Test App</h1>
      <p>If you can see this, React is working!</p>
      <div style={{ marginTop: '20px' }}>
        <h2>Status:</h2>
        <ul>
          <li>✅ React is mounted</li>
          <li>✅ Components are rendering</li>
          <li>✅ JavaScript is working</li>
        </ul>
      </div>
    </div>
  );
};

export default TestApp;
