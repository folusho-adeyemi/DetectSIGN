import cv2
import mediapipe as mp
import numpy as np
import os
import json
from tqdm import tqdm

class DataCollector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        
        self.signs = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
        ]
        
        self.dataset = []
        
    def normalize_landmarks(self, landmarks):
        # Convert to numpy array
        points = np.array([[l.x, l.y, l.z] for l in landmarks])
        
        # Center the points
        centroid = np.mean(points, axis=0)
        centered = points - centroid
        
        # Scale to unit size
        scale = np.max(np.abs(centered))
        normalized = centered / scale
        
        return normalized.flatten()
    
    def is_valid_hand(self, landmarks):
        # Check if hand is facing the camera
        wrist = landmarks[0]
        middle_finger_base = landmarks[9]
        
        # Check if hand is roughly vertical
        if abs(middle_finger_base.y - wrist.y) < 0.1:
            return False
            
        # Check if hand is too close to frame edges
        points = np.array([[l.x, l.y] for l in landmarks])
        if np.any(points < 0.1) or np.any(points > 0.9):
            return False
            
        return True
        
    def collect_samples(self, samples_per_sign=100):
        cap = cv2.VideoCapture(0)
        
        for sign in self.signs:
            print(f"\nCollecting samples for sign: {sign}")
            print("Position your hand clearly in frame")
            print("Press 'SPACE' to capture a sample")
            print("Press 'Q' to skip to next sign")
            
            samples_collected = 0
            
            while samples_collected < samples_per_sign:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                frame_with_hints = frame.copy()
                
                # Draw guide rectangle
                h, w = frame.shape[:2]
                margin = 100
                cv2.rectangle(
                    frame_with_hints,
                    (margin, margin),
                    (w - margin, h - margin),
                    (0, 255, 0),
                    2
                )
                
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    
                    # Draw landmarks
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame_with_hints,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Check hand position
                    is_valid = self.is_valid_hand(hand_landmarks.landmark)
                    status_color = (0, 255, 0) if is_valid else (0, 0, 255)
                    
                    cv2.putText(
                        frame_with_hints,
                        "Hand Position OK" if is_valid else "Adjust Hand Position",
                        (10, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        status_color,
                        2
                    )
                
                # Display instructions and progress
                cv2.putText(
                    frame_with_hints,
                    f"Sign: {sign} - Samples: {samples_collected}/{samples_per_sign}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                cv2.imshow('Data Collection', frame_with_hints)
                key = cv2.waitKey(1)
                
                if key == ord('q'):
                    break
                
                if (key == ord(' ') and results.multi_hand_landmarks and 
                    self.is_valid_hand(results.multi_hand_landmarks[0].landmark)):
                    # Normalize and save features
                    landmarks = results.multi_hand_landmarks[0].landmark
                    features = self.normalize_landmarks(landmarks)
                    
                    self.dataset.append({
                        'features': features.tolist(),
                        'label': sign
                    })
                    
                    samples_collected += 1
                    print(f"Collected sample {samples_collected} for sign {sign}")
                
                elif key == 27:  # ESC
                    cap.release()
                    cv2.destroyAllWindows()
                    return
        
        cap.release()
        cv2.destroyAllWindows()

    def save_dataset(self, filename='hand_signs_dataset.json'):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f)
        print(f"Dataset saved to {filename}")

if __name__ == '__main__':
    collector = DataCollector()
    collector.collect_samples(samples_per_sign=100)
    collector.save_dataset() 