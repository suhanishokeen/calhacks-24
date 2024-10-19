import React from 'react';

const WelcomeRecordCard = ({ name, onRecord }) => {
  return (
    <div 
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Full height of the viewport
        backgroundColor: '#001f4d' // Deep blue background
      }}
    >
      <div 
        style={{
          backgroundColor: '#001f4d', // Card background deep blue
          color: 'white',
          padding: '20px',
          borderRadius: '12px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
          width: '300px',
          textAlign: 'left' // Align text to the left
        }}
      >
        <h2>Welcome back, {name}</h2>
        <p>Glad to see you again! Ask me anything.</p>
        <button 
          onClick={onRecord} 
          style={{
            marginTop: '10px',
            backgroundColor: '#28a745', // Green button
            color: 'white',
            padding: '10px',
            borderRadius: '8px',
            border: 'none',
            cursor: 'pointer',
            width: '100%' // Full-width button
          }}
        >
          Tap to Record
        </button>
      </div>
    </div>
  );
};

export default WelcomeRecordCard;
