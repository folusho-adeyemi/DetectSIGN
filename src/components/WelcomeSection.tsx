import React from 'react';
import './WelcomeSection.css';

interface WelcomeSectionProps {
  username: string;
}

const WelcomeSection: React.FC<WelcomeSectionProps> = ({ username }) => {
  return (
    <div className="welcome-section">
      <div className="welcome-content">
        <div className="welcome-text">
          <h2>Welcome back, {username}!</h2>
          <p>Ready to practice some sign language?</p>
        </div>
        <div className="welcome-animation">
          {/* <img 
            src={waveEmoji} 
            alt="Waving emoji" 
            className="wave-emoji"
          /> */}
        </div>
      </div>
    </div>
  );
};

export default WelcomeSection; 