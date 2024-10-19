import React from 'react';

import WelcomeRecordCard from './components/WelcomeRecordCard';
import SatisfactionRateCard from './components/SatisfactionRateCard';
import ReferralTrackingCard from './components/ReferralTrackingCard';

const Dashboard = () => {
  return (
    <div 
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)', // 3 equal columns for the widgets
        gap: '20px', // Spacing between grid items (widgets)
        padding: '20px',
        height: '100vh',
        backgroundColor: '#001f4d' // Deep blue background for the entire grid
      }}
    >
      {/* First Widget: WelcomeRecordCard */}
      <div 
        style={{
          backgroundColor: '#ffffff', // White background for the widget
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Subtle shadow for elevation
        }}
      >
        <WelcomeRecordCard name="Liza" onRecord={() => console.log('Recording...')} />
      </div>

      {/* Second Widget: SatisfactionRateCard */}
      <div 
        style={{
          backgroundColor: '#ffffff', // White background for the widget
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Subtle shadow for elevation
        }}
      >
        <SatisfactionRateCard />
      </div>

      {/* Third Widget: ReferralTrackingCard */}
      <div 
        style={{
          backgroundColor: '#ffffff', // White background for the widget
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Subtle shadow for elevation
        }}
      >
        <ReferralTrackingCard />
      </div>
    </div>
  );
};

export default Dashboard;
