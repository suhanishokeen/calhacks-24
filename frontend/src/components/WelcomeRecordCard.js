import React from 'react';

const WelcomeRecordCard = ({ name, onRecord }) => {
  return (
    <div 
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Full height of the viewport
        backgroundImage: 'linear-gradient(135deg, #001f4d, #6baeff)', // Outer background gradient
      }}
    >
      <div 
        style={{
          backgroundImage: 'url("/iCal.webp")', // Path to the image in public/ical folder
          backgroundSize: 'cover', // Ensure the image covers the entire background
          backgroundPosition: 'center', // Center the image
          color: 'white',
          padding: '20px',
          borderRadius: '50px',
          boxShadow: '0 20px 45px rgba(0, 0, 0, 0.2)',
          width: '75%',
          height: '65%', 
          display: 'flex',
          flexDirection: 'column', // Stack content vertically
          justifyContent: 'space-between', // Space out the text and the button
        }}
      >
        {/* Welcome text */}
        <div style={{ textAlign: 'left' }}>
          <h1 style={{ opacity: 0.8, fontSize: '32px', marginBottom: '0' }}>
            Welcome back,
          </h1>
          <h1 style={{ color: '#6baeff', fontSize: '36px', marginTop: '0' }}>
            {name}
          </h1>
          <p style={{ fontSize: '18px', marginTop: '10px' }}>
            Glad to see you again! Ask me anything.
          </p>
        </div>

        {/* Button at the bottom */}
        <div 
          style={{
            display: 'flex',
            justifyContent: 'center', // Center the button horizontally
          }}
        >
          <button 
            onClick={onRecord} 
            style={{
              backgroundColor: '#28a745', // Green button
              color: 'white',
              padding: '10px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              width: '100%', // Full-width button
              maxWidth: '200px', // Optional: limit the button width
              textAlign: 'center'
            }}
          >
            Tap to Record
          </button>
        </div>
      </div>
    </div>
  );
};

export default WelcomeRecordCard;
