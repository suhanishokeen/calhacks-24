import React from 'react';
import './styles/styles.css'; 
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MoodCalendarPage from './pages/MoodCalendarPage';
import HomePage from './pages/HomePage';
import AIFriendPage from './pages/AIFriend';
import Tables from './pages/Tables';
import Profile from './pages/Profile';
import Logout from './pages/Logout';
import LoginRegistrationPage from './pages/LoginRegistrationPage';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginRegistrationPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/MoodCalendarPage" element={<MoodCalendarPage />} />
        <Route path="/AIFriend" element={<AIFriendPage />} />
        <Route path="/Tables" element={<Tables />} />
        <Route path="/Profile" element={<Profile />} />
        <Route path="/Logout" element={<Logout />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
