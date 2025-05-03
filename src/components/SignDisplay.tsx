import React, { useState, useEffect } from 'react';
import './SignDisplay.css';

interface SignDisplayProps {
  detectedSign: string;
}

const SignDisplay: React.FC<SignDisplayProps> = ({ detectedSign }) => {
  const [history, setHistory] = useState<string[]>([]);

  useEffect(() => {
    if (detectedSign && detectedSign !== 'Unknown') {
      setHistory(prev => [...prev.slice(-4), detectedSign]);
    }
  }, [detectedSign]);

  return (
    <div className="sign-display">
      <h2>Detected Sign</h2>
      <div className="sign-result">
        {detectedSign || 'No sign detected'}
      </div>
      {history.length > 0 && (
        <div className="sign-history">
          <span>Recent: </span>
          {history.map((sign, index) => (
            <span key={index} className="history-item">{sign}</span>
          ))}
        </div>
      )}
    </div>
  );
};

export default SignDisplay; 