import React from 'react';

// Utility function to calculate the rotation for the circular progress
const calculateRotation = (percentage) => {
  return (percentage / 100) * 360;
};

const ReferralTrackingCard = ({ currentMonth, totalDaysInMonth, daysLoggedInMonth, totalDaysLoggedYear, totalDaysLoggedEver }) => {
  // Calculate the percentage for the circular progress
  const percentageLogged = (daysLoggedInMonth / totalDaysInMonth) * 100;

  return (
    <div 
      style={{
        backgroundColor: '#1a1b2d', // Dark blue background
        padding: '30px',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: '20px',
        backgroundPosition: 'center', // Center the image
        color: '#fff',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 6px 15px rgba(0, 0, 0, 0.3)', // Fancy box-shadow
        width: '75%', // Full width card
        maxWidth: '450px', // Constrained card width
        height: '40%',
        margin: '20px auto' // Centered on the page
      }}
    >
      {/* Left section for total days */}
      <div>
        <div style={{ marginBottom: '20px' }}>
          <p style={{ color: '#a1a4c5', fontSize: '16px' }}>This Year's Commits</p>
          <p style={{ fontSize: '30px', fontWeight: 'bold' }}>{totalDaysLoggedYear}</p>
        </div>
        <div>
          <p style={{ color: '#a1a4c5', fontSize: '16px' }}>Lifetime's Commits</p>
          <p style={{ fontSize: '30px', fontWeight: 'bold' }}>{totalDaysLoggedEver}</p>
        </div>
      </div>

      {/* Right section for circular progress */}
      <div style={{ position: 'relative', width: '120px', height: '120px' }}>
        <div className="circle">
          <div 
            className="circle-inner" 
            style={{
              background: `conic-gradient(#00cc88 ${calculateRotation(percentageLogged)}deg, #2b2c3b 0deg)`, // Green progress
            }}
          >
            <div className="circle-center">
              <p style={{ color: '#fff', fontSize: '18px', margin: '0' }}>
                {daysLoggedInMonth}/{totalDaysInMonth}
              </p>
            </div>
          </div>
        </div>
        <p style={{ color: '#a1a4c5', marginTop: '10px', textAlign: 'center', fontSize: '14px' }}>{currentMonth}</p>
      </div>
    </div>
  );
};

export default ReferralTrackingCard;
