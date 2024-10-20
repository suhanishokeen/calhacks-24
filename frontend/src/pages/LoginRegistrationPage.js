import React, { useState } from 'react';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';
const LoginRegistrationForm = () => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and registration

  // Function to toggle between forms
  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-900 to-purple-600 flex justify-center items-center">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full">
        {isLogin ? <LoginForm /> : <RegistrationForm />}
        <div className="text-center mt-4">
          <button
            className="text-green-500 underline"
            onClick={toggleForm}
          >
            {isLogin ? 'Create an account' : 'Already have an account? Log in'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginRegistrationForm;
