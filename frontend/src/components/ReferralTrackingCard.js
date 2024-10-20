import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const ReferralTrackingCard = ({ currentMonth, totalDaysInMonth, daysLoggedInMonth, totalDaysLoggedYear, totalDaysLoggedEver }) => {
  // Calculate the percentage for the circular progress bar
  const percentageLogged = (daysLoggedInMonth / totalDaysInMonth) * 100;

  return (
    <div
      style={{
        backgroundColor: '#1a1b2d', // Dark blue background
        padding: '20px',
        borderRadius: '15px',
        color: '#fff',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      }}
    >
      {/* Left section for total days */}
      <div>
        <div style={{ marginBottom: '15px' }}>
          <p style={{ color: '#a1a4c5', fontSize: '14px' }}>Total Days Logged This Year</p>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalDaysLoggedYear}</p>
        </div>
        <div>
          <p style={{ color: '#a1a4c5', fontSize: '14px' }}>Total Days Logged Ever</p>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalDaysLoggedEver}</p>
        </div>
        <p style={{ color: '#a1a4c5', marginTop: '10px', textAlign: 'center', fontSize: '14px' }}>{currentMonth}</p>
      </div>

      {/* Right section for circular progress */}
      <div style={{ width: '120px' }}>
        <CircularProgressbar
          value={percentageLogged}
          text={`${daysLoggedInMonth}/${totalDaysInMonth}`}
          styles={buildStyles({
            textColor: '#fff',
            pathColor: '#00cc88',
            trailColor: '#2b2c3b',
            textSize: '16px',
            strokeLinecap: 'round',
          })}
        />
        <p style={{ color: '#a1a4c5', marginTop: '10px', textAlign: 'center' }}>{currentMonth}</p>
      </div>
    </div>
  );
};

export default ReferralTrackingCard;