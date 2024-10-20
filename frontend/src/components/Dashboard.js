import React from 'react';

import WelcomeRecordCard from './components/WelcomeRecordCard';
import SatisfactionRateCard from './components/SatisfactionRateCard';
import ReferralTrackingCard from './components/ReferralTrackingCard';

const Dashboard = () => {
  return (
    <div 
      style={{
        display: 'grid',
        gridTemplateColumns: '50% 25% 25%',
        gap: '20px', // Spacing between grid items (widgets)
        padding: '20px',
        height: '50%',
        backgroundImage: 'linear-gradient(135deg, #001f4d, #6baeff)',
      }}
    >
      {/* First Widget: WelcomeRecordCard */}
      <div>
        <WelcomeRecordCard name="Liza" onRecord={() => console.log('Recording...')} />
      </div>

      {/* Second Widget: ReferralTrackingCard */}
      <div 
        style={{
          borderRadius: '6px',
          padding: '2px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Subtle shadow for elevation
        }}
      >
        <ReferralTrackingCard 
          currentMonth="October"
          totalDaysInMonth={31}
          daysLoggedInMonth={15}
          totalDaysLoggedYear={250}
          totalDaysLoggedEver={600}
          emotions={[
            { name: 'Happiness', percentage: 60 },
            { name: 'Sadness', percentage: 25 },
            { name: 'Surprise', percentage: 15 }
          ]}
        />
      </div>

      {/* Third Widget: SatisfactionRateCard */}
      <div>
        <SatisfactionRateCard />
      </div>
    </div>
  );
};

export default Dashboard;
