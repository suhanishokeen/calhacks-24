import React, { useState, useEffect } from 'react';
import { FaClock } from 'react-icons/fa';

const Header = () => {
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    const intervalId = setInterval(() => {
      const now = new Date();
      const formattedTime = now.toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
      });
      const formattedDate = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
      setCurrentTime({ time: formattedTime, date: formattedDate });
    }, 1000);

    return () => clearInterval(intervalId); 
  }, []);

  return (
    <header className="relative flex items-center p-4 bg-gradient-to-r from-[#0a0034] to-[#180046] text-white shadow-lg">
      {/* Logo and tagline centered */}
      <div className="mx-auto text-center">
        <h1 className="text-6xl font-bold">DayStream</h1>
        <p className="text-sm">Your daily mood tracker</p>
      </div>

      {/* Date and time with styling */}
      <div className="absolute right-4 top-4 text-right px-7">
        <p className="text-s font-semibold flex items-center justify-end">
          <FaClock className="mr-2" /> {currentTime.time}
        </p>
        <p className="text-s bg-gray-700 px-2 py-1 mt-2 rounded-lg">{currentTime.date}</p>
      </div>
    </header>
  );
};

export default Header;
