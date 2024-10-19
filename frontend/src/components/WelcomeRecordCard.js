import React from 'react';

const WelcomeRecordCard = ({ name, onRecord }) => {
  return (
    <div 
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundImage: 'linear-gradient(135deg, #001f4d, #6baeff)', 
      }}
    >
      <div 
        style={{
          backgroundImage: 'url("/iCal.webp")', 
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          color: 'white',
          padding: '20px',
          borderRadius: '50px',
          boxShadow: '0 20px 45px rgba(0, 0, 0, 0.2)',
          width: '75%',
          height: '65%', 
          display: 'flex',
          flexDirection: 'column', 
          justifyContent: 'space-between', 
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
            justifyContent: 'center', 
          }}
        >
          <button 
            onClick={onRecord} 
            style={{
              backgroundColor: '#28a745',
              color: 'white',
              padding: '10px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              width: '100%', 
              maxWidth: '200px',
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