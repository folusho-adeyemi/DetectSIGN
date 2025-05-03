import axios from 'axios';

const API_URL = 'http://localhost:3001';

export interface SignPrediction {
  sign: string;
  confidence: number;
}

export interface DetectionResponse {
  detected: boolean;
  debug_info: string;
  sign_prediction: SignPrediction | null;
  annotated_image?: string;
  error?: string;
}

export const detectHand = async (imageData: string): Promise<DetectionResponse> => {
  const maxRetries = 3;
  let retryCount = 0;

  while (retryCount < maxRetries) {
    try {
      const response = await fetch('http://localhost:3001/detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
      });

      if (response.status === 401) {
        throw new Error('Unauthorized: Invalid API key');
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to detect sign');
      }

      return await response.json();
    } catch (error) {
      retryCount++;
      if (retryCount === maxRetries) {
        console.error('Sign detection error after retries:', error);
        throw error;
      }
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  throw new Error('Failed after maximum retries');
}; 