import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './styles/styles.css';

import WelcomeRecordCard from './components/WelcomeRecordCard';
import SatisfactionRateCard from './components/SatisfactionRateCard';
import ReferralTrackingCard from './components/ReferralTrackingCard';
import MoodCalenderPage from './pages/MoodCalender'; // Import your new page version of MoodCalender

const App = () => {
  return (
    <Router>
      <div className="flex min-h-screen bg-[#0a0034]">
        {/* Sidebar */}
        <div className="w-64 bg-[#1e1e2d] p-5 text-white flex flex-col space-y-4">
          <h2 className="text-2xl font-bold mb-8">Dashboard</h2>
          <nav>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="block p-2 hover:bg-[#38385d] rounded">
                  AI Friend (Welcome Page)
                </Link>
              </li>
              <li>
                <Link to="/mood-table" className="block p-2 hover:bg-[#38385d] rounded">
                  Mood Table
                </Link>
              </li>
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
          <Routes>
            {/* Route for the Welcome Page */}
            <Route path="/" element={
              <div 
                style={{
                  display: 'grid',
                  gridTemplateColumns: '50% 25% 25%',
                  gap: '20px',
                  padding: '20px',
                  height: 'auto',
                  backgroundImage: 'linear-gradient(135deg, #001f4d, #6baeff)',
                  borderRadius: '12px',
                }}
              >
                <div 
                  style={{
                    backgroundColor: '#ffffff',
                    borderRadius: '12px',
                    padding: '20px',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  <WelcomeRecordCard name="Liza" onRecord={() => console.log('Recording...')} />
                </div>
                <div 
                  style={{
                    backgroundColor: '#ffffff',
                    borderRadius: '12px',
                    padding: '20px',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  <ReferralTrackingCard />
                </div>
                <div 
                  style={{
                    backgroundColor: '#ffffff',
                    borderRadius: '12px',
                    padding: '20px',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  <SatisfactionRateCard />
                </div>
              </div>
            } />

            {/* Route for the Mood Table Page */}
            <Route path="/mood-table" element={<MoodCalenderPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
