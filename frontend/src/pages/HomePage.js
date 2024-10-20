import React, { useState } from 'react';
import '../styles/styles.css'; 
import WelcomeRecordCard from '../components/WelcomeRecordCard';
import MoodOverview from '../components/MoodOverview';
import Header from '../components/Header'; 
import Calendar from 'react-calendar'; // Import your calendar component
import ReferralTrackingCard from '../components/ReferralTrackingCard'; // Import the ReferralTrackingCard component

const HomePage = () => {
  const [showCalendar, setShowCalendar] = useState(false); // Manage calendar visibility
  const loggedDays = 20;

  // Sample data for emotions from backend
  const emotions = [
    { name: 'Happiness', percentage: 60 },
    { name: 'Sadness', percentage: 25 },
    { name: 'Surprise', percentage: 15 },
  ];

  // Function to handle "See Calendar" click
  const handleSeeCalendar = () => {
    setShowCalendar(true); // Show the calendar
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-[#0a0034] to-[#180046]">
      <Header />  

      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 bg-[#1e1e2d] p-5 text-white flex flex-col space-y-4">
          <h2 className="text-2xl font-bold mb-8">DASHBOARD</h2>
          <nav>
            <ul className="space-y-2">
              <li><a href="/MoodCalendarPage" className="block p-2 hover:bg-[#38385d] rounded">Mood Calendar</a></li>  
              <li><a href="/AIFriend" className="block p-2 hover:bg-[#38385d] rounded">AI Friend</a></li>            
              <li><a href="/Tables" className="block p-2 hover:bg-[#38385d] rounded">Tables</a></li>
            </ul>
          </nav>
          <p className="mt-8 text-l">Your Account</p>
          <ul className="space-y-2">
            <li><a href="/Profile" className="block p-2 hover:bg-[#38385d] rounded">Profile</a></li>
            <li><a href="/Logout" className="block p-2 hover:bg-[#38385d] rounded">Logout</a></li>
          </ul>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Conditionally render the WelcomeRecordCard or Calendar */}
            <div className="bg-white h-full flex items-center justify-center rounded-lg shadow-lg aspect-square">
              {!showCalendar ? (
                <WelcomeRecordCard 
                  name="Liza" 
                  onRecord={() => console.log('Recording...')} 
                  onSeeCalendar={handleSeeCalendar} // Pass the handler for "See Calendar"
                />
              ) : (
                <div className="p-6 rounded-lg shadow-lg">
                  <Calendar />
                </div>
              )}
            </div>

            {/* Mood Overview Card */}
            <div className="bg-[#234759] p-6 rounded-lg relative">
              <MoodOverview loggedDays={loggedDays} />
            </div>

            {/* Referral Tracking */}
            <div className="bg-gradient-to-br from-[#1e1e2d] to-[#38385d] p-6 rounded-lg shadow-2xl relative">
              <ReferralTrackingCard 
                currentMonth="October" 
                totalDaysInMonth={31} 
                daysLoggedInMonth={15} 
                totalDaysLoggedYear={250} 
                totalDaysLoggedEver={600} 
                emotions={emotions} 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
