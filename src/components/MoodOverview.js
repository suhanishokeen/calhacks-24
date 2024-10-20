import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const MoodOverview = ({ loggedDays }) => {
  const totalDays = 30;
  const percentage = (loggedDays / totalDays) * 100;

  return (
    <div className="p-6 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 bg-[#234759]">
      <h4 className="font-bold text-lg text-white">Happiness Levels</h4>
      <p className="text-white">Your have achieved level:</p>
      
      <div className="flex justify-center items-center mt-4">
        <div className="w-30 h-30">
          <CircularProgressbar
            value={percentage}
            text={`${Math.round(percentage)}%`}
            styles={buildStyles({
              textColor: "#28a745", 
              pathColor: "#28a745", 
              trailColor: "#000000", 
            })}
          />
        </div>
      </div>
    </div>
  );
};

export default MoodOverview;
