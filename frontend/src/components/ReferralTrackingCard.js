
import React from 'react';

const ReferralTrackingCard = ({ invited, bonus, safetyScore }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <h3 className="font-bold">Referral Tracking</h3>
      <div className="mt-2">
        <p>Invited: {invited} people</p>
        <p>Bonus: {bonus}</p>
      </div>
      <div className="mt-4">
        <h4>Safety</h4>
        <div className="text-2xl">{safetyScore}</div>
        <div className="w-full h-2 bg-gray-200 rounded">
          <div
            className="h-full bg-green-500 rounded"
            style={{ width: `${(safetyScore / 10) * 100}%` }} // Assuming max score is 10
          />
        </div>
      </div>
    </div>
  );
};

export default ReferralTrackingCard;
