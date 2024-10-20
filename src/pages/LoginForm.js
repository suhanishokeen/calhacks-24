import React, { useState } from 'react';
import axios from 'axios'; // Make sure axios is installed
const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const loginData = { email, password };

    try {
      const response = await axios.post('http://localhost:5000/login', loginData); // Replace with your backend login route
      console.log('Login successful:', response.data);

      // Handle successful login (e.g., store token, redirect user)
      localStorage.setItem('token', response.data.token); // Store token in localStorage or state management
      window.location.href = '/dashboard'; // Redirect to dashboard

    } catch (error) {
      console.error('Error logging in:', error);
      // Handle login error (e.g., show error message)
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">Log In</h2>
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
        Log In
      </button>
    </form>
  );
};

export default LoginForm;
