import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './AuthPage.css';

const AuthPage: React.FC = () => {
  const [isSignIn, setIsSignIn] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const endpoint = isSignIn ? 'login' : 'register';
      const body = isSignIn 
        ? { username, password }
        : { username, email, password };

      const response = await fetch(`http://localhost:3001/auth/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Failed to ${isSignIn ? 'sign in' : 'sign up'}`);
      }

      login(data.user);
      localStorage.setItem('token', data.token);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-content">
        <div className="auth-left">
          <h1>ASL Detection App</h1>
          <p className="subtitle">Learn and practice American Sign Language with real-time detection</p>
          <div className="features">
            <div className="feature">
              <span className="feature-icon">👋</span>
              <h3>Real-time Detection</h3>
              <p>Instant feedback on your hand signs</p>
            </div>
            <div className="feature">
              <span className="feature-icon">🎮</span>
              <h3>Interactive Games</h3>
              <p>Learn while having fun</p>
            </div>
            <div className="feature">
              <span className="feature-icon">📊</span>
              <h3>Track Progress</h3>
              <p>Monitor your learning journey</p>
            </div>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-box">
            <div className="auth-toggle">
              <button 
                className={isSignIn ? 'active' : ''} 
                onClick={() => setIsSignIn(true)}
              >
                Sign In
              </button>
              <button 
                className={!isSignIn ? 'active' : ''} 
                onClick={() => setIsSignIn(false)}
              >
                Sign Up
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              {error && <div className="error-message">{error}</div>}
              
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>

              {!isSignIn && (
                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              )}

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <button type="submit" className="submit-button">
                {isSignIn ? 'Sign In' : 'Sign Up'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage; 