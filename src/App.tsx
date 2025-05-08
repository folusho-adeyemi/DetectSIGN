import React, { useState } from 'react';
import Camera from './components/Camera';
import SignDisplay from './components/SignDisplay';
import SpellingGame from './components/SpellingGame';
import ThemeToggle from './components/ThemeToggle';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import { detectHand } from './services/modelService';
import { AuthProvider, useAuth } from './context/AuthContext';
import AuthPage from './components/AuthPage';
import UserMenu from './components/UserMenu';
import WelcomeSection from './components/WelcomeSection';
import './App.css';

const AppContent: React.FC = () => {
  const { user } = useAuth();
  const { isDarkMode } = useTheme();
  const [detectedSign, setDetectedSign] = useState<string>('');
  const [debugImage, setDebugImage] = useState<string | undefined>();
  const [currentSign, setCurrentSign] = useState<string>('');

  const handleFrame = async (imageDataUrl: string) => {
    try {
      const result = await detectHand(imageDataUrl);
      
      if (result.detected && result.sign_prediction) {
        const confidence = (result.sign_prediction.confidence * 100).toFixed(1);
        setDetectedSign(`Sign: ${result.sign_prediction.sign} (${confidence}%)`);
        setCurrentSign(result.sign_prediction.sign);
        
        if (result.annotated_image) {
          setDebugImage(result.annotated_image);
        }
      } else {
        setDetectedSign('No Sign Detected');
        setDebugImage(undefined);
      }
    } catch (error) {
      console.error('Error detecting sign:', error);
      setDetectedSign('Error detecting sign');
      setDebugImage(undefined);
    }
  };

  const handleGameEnd = (score: number) => {
    console.log(`Game ended with score: ${score}`);
  };

  if (!user) {
    return <AuthPage />;
  }

  return (
    <div className={`App ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <header className="App-header">
        <h1>DetectSIGN</h1>
        <div className="header-actions">
          <ThemeToggle />
          <UserMenu />
        </div>
      </header>
      
      <WelcomeSection username={user.username} />
      
      <main>
        <div className="instructions">
          <p>Position your hand in front of the camera and make an ASL sign. 
             The detector will attempt to recognize the sign in real-time.</p>
        </div>
        <div className="detection-container">
          <div className="camera-section">
            <Camera onFrame={handleFrame} />
            <SignDisplay detectedSign={detectedSign} />
            <SpellingGame 
              currentSign={currentSign}
              onGameEnd={handleGameEnd}
            />
          </div>
          {debugImage && (
            <div className="debug-image-section">
              <h3>Detection Result</h3>
              <img 
                src={debugImage} 
                alt="Sign detection visualization" 
                className="debug-image"
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </AuthProvider>
  );
};

export default App; 