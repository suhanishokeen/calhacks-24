import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css'; // Default calendar styles
import '../styles/styles.css'; // Your custom styles from src/styles/styles.css

const MoodCalendar = () => {
  const [date, setDate] = useState(new Date());

  return (
    <div className="calendar-container p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-4">Mood Calender</h1>
      <Calendar
        onChange={setDate}
        value={date}
        className="fancy-calendar" // Add class if needed for customization
      />
      <div className="mt-4 text-center">
        <p className="text-lg">Selected date: {date.toDateString()}</p>
      </div>
    </div>
  );
};

export default MoodCalendar;
