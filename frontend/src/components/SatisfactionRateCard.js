// src/components/SatisfactionRateCard.js
import React from 'react';

const SatisfactionRateCard = ({ rate }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg transition duration-300 ease-in-out transform hover:scale-105">
      <h3 className="font-bold text-lg text-gray-800">Satisfaction Rate</h3>
      <p className="text-gray-600">From all projects</p>
      <div className="flex flex-col items-center mt-4">
        <div className="text-4xl text-blue-600">{rate}%</div>
        <span className="text-gray-500">Based on likes</span>
      </div>
      <div className="mt-2">
        <div className="w-full h-2 bg-gray-200 rounded">
          <div
            className="h-full bg-blue-500 rounded"
            style={{ width: `${rate}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default SatisfactionRateCard;
