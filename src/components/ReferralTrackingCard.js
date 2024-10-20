import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const ReferralTrackingCard = ({
  currentMonth,
  totalDaysInMonth,
  daysLoggedInMonth,
  totalDaysLoggedYear,
  totalDaysLoggedEver,
  emotions,
}) => {
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
        flexDirection: 'column',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        maxWidth: '400px',
      }}
    >
      {/* Circular Progress for Days Logged */}
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between' }}>
        <div>
          <p style={{ color: '#a1a4c5', fontSize: '14px' }}>Total Days Logged This Year</p>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalDaysLoggedYear}</p>
          <p style={{ color: '#a1a4c5', fontSize: '14px' }}>Total Days Logged Ever</p>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalDaysLoggedEver}</p>
        </div>

        <div style={{ width: '100px' }}>
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
        </div>
      </div>

      {/* Emotions Section with Green Percentage Bars */}
      <div style={{ marginTop: '20px' }}>
        <h3 style={{ color: '#fff', fontSize: '18px', marginBottom: '10px' }}>Top 4 Emotions</h3>
        {emotions.map((emotion, index) => (
          <div key={index} style={{ marginBottom: '15px' }}>
            <p style={{ color: '#a1a4c5', fontSize: '14px', marginBottom: '5px' }}>
              {emotion.name}: {emotion.percentage}%
            </p>
            <div
              style={{
                backgroundColor: '#2b2c3b',
                borderRadius: '10px',
                height: '10px',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${emotion.percentage}%`,
                  backgroundColor: '#00cc88',
                  height: '100%',
                  borderRadius: '10px',
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReferralTrackingCard;