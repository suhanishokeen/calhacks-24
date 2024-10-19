import React from 'react';
import { Link } from 'react-router-dom'; // Ensure you have react-router-dom installed if you're using routing

const Header = () => {
  return (
    <header className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <h1 className="text-xl">Your App Name</h1>
      <nav>
        <ul className="flex space-x-4">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/sign-in">Sign In</Link></li>
          {/* Add more links as necessary */}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
