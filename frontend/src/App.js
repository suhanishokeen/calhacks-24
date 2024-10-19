import React from 'react';
import './styles/styles.css'; 

import WelcomeRecordCard from './components/WelcomeRecordCard';
import SatisfactionRateCard from './components/SatisfactionRateCard';
import ReferralTrackingCard from './components/ReferralTrackingCard';

const App = () => {
  return (
    <div className="flex min-h-screen bg-[#0a0034]">
      {/* Sidebar */}
      <div className="w-64 bg-[#1e1e2d] p-5 text-white flex flex-col space-y-4">
        <h2 className="text-2xl font-bold mb-8">Dashboard</h2>
        <nav>
          <ul className="space-y-2">
            <li><a href="#" className="block p-2 hover:bg-[#38385d] rounded">AI Friend</a></li>
            <li><a href="#" className="block p-2 hover:bg-[#38385d] rounded">Tables</a></li>
          </ul>
        </nav>
        <h3 className="mt-8 text-xl">Account Pages</h3>
        <ul className="space-y-2">
          <li><a href="#" className="block p-2 hover:bg-[#38385d] rounded">Profile</a></li>
          <li><a href="#" className="block p-2 hover:bg-[#38385d] rounded">Logout</a></li>
        </ul>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-8">
        {/* Grid layout for widgets */}
        <div 
          style={{
            display: 'grid',
            gridTemplateColumns: '50% 25% 25%',
            gap: '20px', // Spacing between grid items (widgets)
            padding: '20px',
            height: 'auto', // Adjust the height of the grid layout
            backgroundImage: 'linear-gradient(135deg, #001f4d, #6baeff)',
            borderRadius: '12px',
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

          {/* Second Widget (now swapped): ReferralTrackingCard */}
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

          {/* Third Widget (now swapped): SatisfactionRateCard */}
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
        </div>
      </div>
    </div>
  );
};

export default App;
