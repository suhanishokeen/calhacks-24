import React, { useState } from 'react';

const AIChat = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isThinking, setIsThinking] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      setChatHistory([...chatHistory, { sender: 'user', text: message }]);
      setMessage('');
      
      setIsThinking(true); 

      setTimeout(() => {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { sender: 'ai', text: 'AI is thinking...' }
        ]);
        setIsThinking(false);
      }, 1000);
    }
  };

  return (
    <div>
      <h1>AI Diary</h1> {/* Title */}
      
      {/* Chat window */}
      <div className="chat-window">
        {chatHistory.map((chat, index) => (
          <div key={index} className={chat.sender}>
            <p><strong>{chat.sender === 'user' ? 'You: ' : 'AI: '}</strong>{chat.text}</p>
          </div>
        ))}
      </div>

      
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={message} 
          onChange={(e) => setMessage(e.target.value)} 
          placeholder="Type your message..." 
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default AIChat;
