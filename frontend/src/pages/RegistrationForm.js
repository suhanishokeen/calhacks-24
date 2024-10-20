import React, { useState } from 'react';
import axios from 'axios';


const RegistrationForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newUser = { username, email, password };

    try {
      const response = await axios.post('http://localhost:5000/register', newUser);
      console.log('User registered successfully:', response.data);
    } catch (error) {
      console.error('Error registering user:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2 className="text-2xl font-bold text-white mb-6 text-center">Sign Up</h2>
      <div className="mb-4">
        <label className="block text-gray-400 mb-2">Username</label>
        <input
          type="text"
          className="w-full p-2 rounded-md bg-gray-700 text-white focus:ring-2 focus:ring-green-500"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
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
    </form>
  );
};

export default RegistrationForm;
