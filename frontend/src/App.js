import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import AIChat from './components/AIChat';
import MoodCalendar from './components/MoodCalendar';
import PulseAnimation from './components/PulseAnimation';

function App() {

  return (
    <Router>
      <div className="App">
        {/* Taskbar at the top */}
        <nav>
          <ul className="taskbar">
            <li><Link to="/chat">AI Chat</Link></li>
            <li><Link to="/calendar">Mood Calendar</Link></li>
            <li><Link to="/history">Mood History</Link></li>
          </ul>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route path="/chat" element={<AIChat />} />
          <Route path="/calendar" element={<MoodCalendar />} />
          <Route path="/" element={<AIChat />} /> 
          <Route path="/" element={<PulseAnimation />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
