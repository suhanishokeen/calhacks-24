import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [credentials, setCredentials] = useState({ username: '', email: '', password: '' });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [typedText, setTypedText] = useState('');
  const fullText = "Welcome to DayStream - Your daily mood tracker.";
  const navigate = useNavigate();

  useEffect(() => {
    let currentIndex = 0;
    const typeLetter = () => {
      if (currentIndex < fullText.length) {
        setTypedText((prev) => prev + fullText[currentIndex]);
        currentIndex++;
      }
    };

    const typingInterval = setInterval(typeLetter, 100);
    return () => clearInterval(typingInterval);
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (credentials.username === 'testUser' && credentials.password === 'password123') {
      setIsAuthenticated(true);
      navigate('/dashboard');
    } else {
      alert('Invalid credentials, please try again.');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials({
      ...credentials,
      [name]: value,
    });
  };

  return (
    <div className="login-page-container">
      <div className="left-half">
        <div className="login-container">
          <form onSubmit={handleLogin}>
            <div>
              <label>Username:</label>
              <input
                type="text"
                name="username"
                value={credentials.username}
                onChange={handleInputChange}
                required
              />
            </div>
            <div>
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={credentials.email}
                onChange={handleInputChange}
                required
              />
            </div>
            <div>
              <label>Password:</label>
              <input
                type="password"
                name="password"
                value={credentials.password}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="button-group">
              <button type="submit" className="sign-in-btn">Sign In</button>
              <button type="button" className="login-btn" onClick={handleLogin}>Login</button>
            </div>
          </form>
        </div>
      </div>
      <div className="right-half">
        <p className="typewriter-text">{typedText}</p>
      </div>
    </div>
  );
};

export default Login;