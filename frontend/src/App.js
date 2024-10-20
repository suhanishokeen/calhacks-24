import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MoodCalendarPage from './pages/MoodCalendarPage';
import AIFriendPage from './pages/AIFriend';
import Tables from './pages/Tables';
import Profile from './pages/Profile';
import Logout from './components/Logout';
import LoginRegistrationPage from './pages/LoginRegistrationPage';
import RegistrationForm from './pages/RegistrationForm';
import ProtectedRoute from './components/ProtectedRoute'; // Import ProtectedRoute

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LoginRegistrationPage />} />
        <Route path="/register" element={<RegistrationForm />} />

        {/* Protected Routes */}
        <Route 
          path="/home" 
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/moodcalendar" 
          element={
            <ProtectedRoute>
              <MoodCalendarPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/aifriend" 
          element={
            <ProtectedRoute>
              <AIFriendPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/tables" 
          element={
            <ProtectedRoute>
              <Tables />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/profile" 
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          } 
        />
        <Route path="/logout" element={<Logout />} />
        

      </Routes>
    </BrowserRouter>
  );
};

export default App;
