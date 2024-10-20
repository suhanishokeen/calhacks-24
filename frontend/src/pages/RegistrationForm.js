import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // Import useNavigate

const RegistrationForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  
  const navigate = useNavigate();  // Initialize useNavigate

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newUser = { username, email, password };

    try {
      const response = await axios.post('https://13e2-199-115-241-193.ngrok-free.app/auth/register', newUser);  // Use Flask API URL
      console.log('User registered successfully:', response.data);
      setMessage('Registration successful!');
      
      // Redirect to /Home after successful registration
      navigate('/');
    } catch (error) {
      console.error('Error registering user:', error);
      setMessage(error.response?.data.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">Sign Up</h2>

      <div className="mb-4">
        <label className="block text-gray-400 mb-2">Email</label>
        <input
          type="email"
          className="w-full p-2 rounded-md bg-gray-700 text-white focus:ring-2 focus:ring-green-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-400 mb-2">Password</label>
        <input
          type="password"
          className="w-full p-2 rounded-md bg-gray-700 text-white focus:ring-2 focus:ring-green-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button
        type="submit"
        className="w-full bg-green-500 hover:bg-green-600 text-white p-2 rounded-md mt-4"
      >
        Sign Up
      </button>

      {message && <p className="mt-4 text-center text-red-500">{message}</p>}
    </form>
  );
};

export default RegistrationForm;
