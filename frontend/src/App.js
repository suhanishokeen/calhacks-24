import React from 'react';
import Header from './components/Header';
import SignIn from './components/SignIn';
import WelcomeRecordCard from './components/WelcomeRecordCard'; // If you want to keep this
import SatisfactionRateCard from './components/SatisfactionRateCard'; // Optional, as needed
import ReferralTrackingCard from './components/ReferralTrackingCard'; // Optional, as needed
import Sidebar from './components/Sidebar';
import { useAuthContext } from "./hooks/useAuthContext"

const App = () => {
  const handleRecord = () => {
    // Logic to start recording with Hume.ai
    console.log('Recording started...');
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-4">
        <Header />
        <SignIn />
        <WelcomeRecordCard name="Mark Johnson" onRecord={handleRecord} />
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <SatisfactionRateCard rate={95} />
          <ReferralTrackingCard invited={145} bonus={1465} safetyScore={9.3} />
          {/* Add more cards here as needed */}
        </div>
      </div>
    </div>
  );
};

export default App;
