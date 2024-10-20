import React from 'react';
import './styles/styles.css'; 
//import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MoodCalendarPage from './pages/MoodCalendarPage';
import HomePage from './pages/HomePage';
import AIFriendPage from './pages/AIFriend';
import Tables from './pages/Tables';
import Profile from './pages/Profile';
import Logout from './pages/Logout';
import Login from './pages/Login';
import Dashboard from './components/Dashboard';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/MoodCalendarPage" element={<MoodCalendarPage />} />
        <Route path="/AIFriend" element={<AIFriendPage />} />
        <Route path="/Tables" element={<Tables />} />
        <Route path="/Profile" element={<Profile />} />
        <Route path="/Logout" element={<Logout />} />
        <Route path="/dashboard" element={<Dashboard />} /> {/* Updated path */}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
