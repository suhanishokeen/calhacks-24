import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';  // Import the useNavigate hook
import '../styles/styles.css';  // Import the new AIFriend.css file

const AIFriendPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioChunks, setAudioChunks] = useState([]);
  const mediaRecorderRef = useRef(null);
  const navigate = useNavigate();  // Create navigate function to redirect

  // Start recording audio
  const startRecording = async () => {
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = (event) => {
      setAudioChunks((prev) => [...prev, event.data]);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      sendAudioToBackend(audioBlob); // Send audio to the backend
      setAudioChunks([]); // Reset audio chunks for next recording
    };

    mediaRecorder.start();
  };

  // Stop recording audio
  const stopRecording = () => {
    setIsRecording(false);
    mediaRecorderRef.current.stop();
  };

  // Function to send the audio file to the backend
  const sendAudioToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, `recording-${Date.now()}.wav`);

    try {
      const response = await fetch('https://13e2-199-115-241-193.ngrok-free.app/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('Audio file uploaded successfully');
      } else {
        console.error('Error uploading audio file');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  // Function to navigate back to the home page
  const goToHomePage = () => {
    navigate('/');  // Navigate to the home page (assuming your home route is '/')
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
};

export default AIFriendPage;
