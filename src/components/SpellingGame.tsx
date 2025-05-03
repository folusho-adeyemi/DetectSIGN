import React, { useState, useEffect } from 'react';
import './SpellingGame.css';

interface SpellingGameProps {
  currentSign: string;
  onGameEnd?: (score: number) => void;
}

const SpellingGame: React.FC<SpellingGameProps> = ({ currentSign, onGameEnd }) => {
  const [currentWord, setCurrentWord] = useState<string>('');
  const [targetWord, setTargetWord] = useState<string>('');
  const [score, setScore] = useState<number>(0);
  const [timeLeft, setTimeLeft] = useState<number>(30);
  const [gameActive, setGameActive] = useState<boolean>(false);
  const [wordList] = useState<string[]>([
    'HELLO', 'WORLD', 'SIGN', 'LEARN', 'PLAY',
    'GAME', 'HAND', 'SPELL', 'CODE', 'FUN'
  ]);

  useEffect(() => {
    if (gameActive && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => prev - 1);
      }, 1000);
      return () => clearInterval(timer);
    } else if (timeLeft === 0) {
      endGame();
    }
  }, [timeLeft, gameActive]);

  useEffect(() => {
    if (gameActive && currentSign) {
      setCurrentWord(prev => {
        const newWord = prev + currentSign;
        if (newWord === targetWord) {
          setScore(prev => prev + 10);
          selectNewWord();
          return '';
        }
        return newWord;
      });
    }
  }, [currentSign, gameActive]);

  const startGame = () => {
    setGameActive(true);
    setScore(0);
    setTimeLeft(30);
    setCurrentWord('');
    selectNewWord();
  };

  const endGame = () => {
    setGameActive(false);
    if (onGameEnd) {
      onGameEnd(score);
    }
  };

  const selectNewWord = () => {
    const newWord = wordList[Math.floor(Math.random() * wordList.length)];
    setTargetWord(newWord);
  };

  return (
    <div className="spelling-game">
      <div className="game-header">
        <div className="score">Score: {score}</div>
        <div className="timer">Time: {timeLeft}s</div>
      </div>

      {!gameActive ? (
        <div className="game-start">
          <h2>Spelling Game</h2>
          <p>Spell the words using sign language!</p>
          <button onClick={startGame}>Start Game</button>
        </div>
      ) : (
        <div className="game-content">
          <div className="target-word">
            <h3>Spell:</h3>
            <div className="word">{targetWord}</div>
          </div>
          <div className="current-word">
            <h3>Your spelling:</h3>
            <div className="word">{currentWord}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SpellingGame; 