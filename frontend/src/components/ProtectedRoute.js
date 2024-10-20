import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('token'); // Check if the token is stored in localStorage

  if (!isAuthenticated) {
    // If the user is not authenticated, redirect them to the login page
    return <Navigate to="/" />;
  }

  // If the user is authenticated, allow access to the protected route
  return children;
};

export default ProtectedRoute;
