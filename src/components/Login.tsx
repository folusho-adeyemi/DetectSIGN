import React from 'react';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login: React.FC = () => {
  const { loginWithGithub } = useAuth();

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Sign In</h2>
        <p>Track your progress and save your results</p>
        <button 
          className="github-button"
          onClick={loginWithGithub}
        >
          <i className="fab fa-github"></i>
          Continue with GitHub
        </button>
      </div>
    </div>
  );
};

export default Login; 