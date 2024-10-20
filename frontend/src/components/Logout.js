import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear user data (e.g., token) from localStorage
    localStorage.removeItem('token');

    // Redirect the user to the login page
    navigate('/');
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <p>Logging you out...</p>
    </div>
  );
};

export default Logout;
