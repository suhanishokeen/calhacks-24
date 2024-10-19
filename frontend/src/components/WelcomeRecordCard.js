import React from 'react';

const WelcomeRecordCard = ({ name, onRecord }) => {
  return (
    <div className="bg-blue-600 text-white p-4 rounded-lg shadow-lg">
      <h2>Welcome back, {name}</h2>
      <p>Glad to see you again! Ask me anything.</p>
      <button 
        onClick={onRecord} 
        className="mt-4 bg-green-500 text-white p-2 rounded">
        Tap to Record
      </button>
    </div>
  );
};

export default WelcomeRecordCard;
