import React from 'react';
//import AIChat from './components/AIChat'; // If you want to keep this
//import MoodCalendar from './components/MoodCalendar'; // If you want to keep this
import WelcomeRecordCard from './components/WelcomeRecordCard';
import SatisfactionRateCard from './components/SatisfactionRateCard';
import ReferralTrackingCard from './components/ReferralTrackingCard';
//import Sidebar from './components/Sidebar';

const App = () => {
  const handleRecord = () => {
    // Logic to start recording with Hume.ai
    console.log('Recording started...');
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-4">
        <WelcomeRecordCard name="Mark Johnson" onRecord={handleRecord} />
        
        {/* Add the grid layout for the cards here */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <SatisfactionRateCard rate={95} />
          <ReferralTrackingCard invited={145} bonus={1465} safetyScore={9.3} />
          {/* You can add more cards here as needed */}
        </div>
        
        <MoodCalendar />
        <AIChat />
      </div>
    </div>
  );
};

export default App;
