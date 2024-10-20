import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';  // Import the useNavigate hook
import '../styles/styles.css';  // Import the styles
import Recorder from 'recorder-js';

const AIFriendPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const recorderRef = useRef(null);
  const navigate = useNavigate();
  const [audioChunks, setAudioChunks] = useState([]);
  const mediaRecorderRef = useRef(null);

  const startRecording = async () => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const recorder = new Recorder(audioContext);

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder.init(stream);

    recorderRef.current = recorder;
    recorder.start();
    setIsRecording(true);
  };

  const stopRecording = async () => {
    const { blob, buffer } = await recorderRef.current.stop();
    setIsRecording(false);
    sendAudioToBackend(blob);
  };

  const sendAudioToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append('file', audioBlob, `recording-${Date.now()}.wav`);
    console.log('audioBlob type:', audioBlob.type);
    const token = localStorage.getItem('jwt_token');
    try {
      const response = await fetch('https://13e2-199-115-241-193.ngrok-free.app/upload-audio', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzE1MDZlN2VhZGUxYzg2YTgxMmYzMDIiLCJleHAiOjE3Mjk0MzMzNzl9.PCMokuPO6WfbIihnfzxUJqZPPzfEtvYqxsDckPH09zE`,  // Hardcoded JWT token
        },
        body: formData,
      });

      if (response.ok) {
        console.log('Audio file uploaded successfully');
        // Handle successful response
      } else {
        const errorData = await response.json();
        console.error('Error uploading audio file:', errorData);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  // Function to navigate back to the HomePage.js
  const goToHomePage = () => {
    navigate('/home');  // Navigate to the HomePage.js route
  };

  return (
    <div className="aifriend-container">
      {/* Cross button at the top-right corner */}
      <button className="close-button" onClick={goToHomePage}>✖</button>

      {/* AI Avatar */}
      <div className="avatar-container">
        <img src="/Cloud.png" alt="Friendly AI" className="ai-avatar pulsate" />
        <div className="ai-title-box">
          <h2 className="ai-title">Veronica</h2>
        </div>
      </div>

      {/* Controls for Recording */}
      <div className="controls-container">
        {!isRecording && (
          <button className="control-button start-button" onClick={startRecording}>
            Start Recording
          </button>
        )}

        {isRecording && (
          <button className="control-button stop-button" onClick={stopRecording}>
            ⏹ Stop Recording
          </button>
        )}
      </div>
    </div>
  );
  // Rest of your component code...
};
export default AIFriendPage;  // Export the AIFriendPage component