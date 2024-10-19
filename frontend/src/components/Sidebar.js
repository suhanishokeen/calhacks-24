import React from 'react';
import { Link } from 'react-router-dom'; // Ensure you have react-router-dom installed

const Sidebar = () => {
  return (
    <nav className="bg-gray-800 text-white w-64 min-h-screen p-4">
      <h1 className="text-xl mb-6">Your App Name</h1>
      <ul>
        <li className="mb-4">
          <Link to="/" className="hover:text-blue-300">Dashboard</Link>
        </li>
        <li className="mb-4">
          <Link to="/about" className="hover:text-blue-300">About</Link>
        </li>
        <li className="mb-4">
          <Link to="/sign-in" className="hover:text-blue-300">Sign In</Link>
        </li>
        <li className="mb-4">
          <Link to="/mood-calendar" className="hover:text-blue-300">Mood Calendar</Link>
        </li>
        <li className="mb-4">
          <Link to="/ai-chat" className="hover:text-blue-300">AI Chat</Link>
        </li>
        {/* Add more links as necessary */}
      </ul>
    </nav>
  );
};

export default Sidebar;
