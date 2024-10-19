import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const MoodCalendar = () => {
  const [date, setDate] = useState(new Date());
  const [moodLog, setMoodLog] = useState({});

  const handleDayClick = (selectedDate) => {
    const mood = prompt("How do you feel today? (happy, neutral, sad)");
    if (mood) {
      setMoodLog({
        ...moodLog,
        [selectedDate.toDateString()]: mood
      });
    }
  };

  const tileClassName = ({ date, view }) => {
    if (view === 'month') {
      const mood = moodLog[date.toDateString()];
      if (mood === 'happy') {
        return 'happy-day'; // Style for happy days
      } else if (mood === 'sad') {
        return 'sad-day'; // Style for sad days
      }
    }
    return null;
  };

  return (
    <div>
      <h2>Mood Calendar</h2>
      <Calendar
        onClickDay={handleDayClick}
        value={date}
        tileClassName={tileClassName}
      />
    </div>
  );
};

export default MoodCalendar;
