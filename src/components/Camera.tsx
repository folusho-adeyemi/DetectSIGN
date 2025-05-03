import React, { useEffect, useRef, useState } from 'react';
import './Camera.css';
import { detectHand } from '../services/modelService';

interface CameraProps {
  onFrame: (imageDataUrl: string) => Promise<void>;
}

const Camera: React.FC<CameraProps> = ({ onFrame }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startCamera = async () => {
    const videoElement = videoRef.current;
    const canvasElement = canvasRef.current;
    
    if (!videoElement || !canvasElement) return;
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: 640,
          height: 480,
          frameRate: { ideal: 10 }  // Limit frame rate
        } 
      });
      
      videoElement.srcObject = stream;
      streamRef.current = stream;
      await videoElement.play();
      setIsStreaming(true);

      canvasElement.width = videoElement.videoWidth;
      canvasElement.height = videoElement.videoHeight;

      const context = canvasElement.getContext('2d', { willReadFrequently: true });
      
      // Modified interval for frame capture
      intervalRef.current = setInterval(() => {
        if (context && videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
          // Draw the frame
          context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
          
          // Convert to base64 directly instead of using ImageData
          const imageDataUrl = canvasElement.toDataURL('image/jpeg', 0.7);
          
          // Pass the base64 string to onFrame
          onFrame(imageDataUrl).catch(console.error);
        }
      }, 2000); // Increased to 2 seconds
    } catch (error) {
      console.error('Error accessing the camera:', error);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsStreaming(false);
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="camera-container">
      <video 
        ref={videoRef} 
        className="camera-video"
        playsInline
      />
      <canvas 
        ref={canvasRef} 
        className="camera-canvas"
      />
      <div className="camera-controls">
        {!isStreaming ? (
          <button onClick={startCamera} className="camera-button">
            Start Camera
          </button>
        ) : (
          <button onClick={stopCamera} className="camera-button">
            Stop Camera
          </button>
        )}
      </div>
    </div>
  );
};

export default Camera; 