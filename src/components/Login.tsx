import React from 'react';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login: React.FC = () => {
  const { login } = useAuth();

  // Create a handler function that wraps the login call
  const handleLogin = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    // Here you should fetch user data from your API
    // For now, using mock data to make it work
    login({
      id: '1',
      username: 'user',
      email: 'user@example.com'
    });
  };

  return (
    <div className="login-container">
      <div className="brand-container">
        <h1>DetectSIGN</h1>
        <p>Learn and master American Sign Language through interactive recognition</p>
      </div>
      
      <div className="login-card">
        <h2>Welcome Back</h2>
        <p>Sign in to track your progress and access all features</p>
        
        <div className="login-options">
          <button 
            className="login-button github-button"
            onClick={handleLogin}
          >
            <i className="fab fa-github"></i>
            <span>Continue with GitHub</span>
          </button>
          
          <button 
            className="login-button google-button"
            onClick={handleLogin}
          >
            <i className="fab fa-google"></i>
            <span>Continue with Google</span>
          </button>
          
          <div className="divider">
            <span>or</span>
          </div>
          
          <button 
            className="login-button email-button"
            onClick={handleLogin}
          >
            <i className="far fa-envelope"></i>
            <span>Continue with Email</span>
          </button>
        </div>
        
        <div className="login-footer">
          <p>Don't have an account? <a href="#">Sign up</a></p>
        </div>
      </div>
    </div>
  );
};

export default Login;