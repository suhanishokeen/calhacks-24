import React from 'react';
import MoodCalendar from '../components/MoodCalendar'; // Import the renamed MoodCalendar component

const MoodCalendarPage = () => {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-blue-500 to-blue-800 p-6">
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-blue-900 mb-6">Mood Calendar</h1>
        <MoodCalendar /> {/* Render the MoodCalendar component here */}
      </div>
    </div>
  );
};

export default MoodCalendarPage;
