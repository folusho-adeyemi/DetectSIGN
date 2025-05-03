from flask import request, jsonify
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import cv2
import mediapipe as mp
import tensorflow as tf
import pickle

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Load pre-trained model and preprocessing tools
try:
    model = tf.keras.models.load_model('hand_sign_model.keras')
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("Model and preprocessing tools loaded successfully!")
except Exception as e:
    print(f"Error loading model or preprocessing tools: {e}")

def normalize_landmarks(landmarks):
    points = np.array([[l.x, l.y, l.z] for l in landmarks])
    centroid = np.mean(points, axis=0)
    centered = points - centroid
    scale = np.max(np.abs(centered))
    normalized = centered / scale
    return normalized.flatten()

def extract_features(landmarks):
    features = normalize_landmarks(landmarks)
    features = features.reshape(1, -1)
    features_scaled = scaler.transform(features)
    return features_scaled

def classify_hand_sign(landmarks):
    try:
        features = extract_features(landmarks)
        prediction = model.predict(features, verbose=0)
        predicted_class = label_encoder.inverse_transform([np.argmax(prediction)])[0]
        confidence = float(np.max(prediction))
        return predicted_class, confidence
    except Exception as e:
        print(f"Error in classification: {e}")
        return "Unknown", 0.0

def detect():
    try:
        # Get the image data from request
        image_data = request.json['image']
        
        # Initialize response
        result = {
            'detected': False,
            'debug_info': 'No hand detected',
            'sign_prediction': None,
            'annotated_image': None
        }

        # Process image data
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(image)
        image_array = cv2.flip(image_array, 1)

        # Process the image
        results = hands.process(image_array)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            sign, confidence = classify_hand_sign(hand_landmarks.landmark)

            result['detected'] = True
            result['sign_prediction'] = {
                'sign': sign,
                'confidence': confidence
            }
            result['debug_info'] = f"Detected sign: {sign} ({confidence:.2%} confidence)"

            # Create debug image
            debug_image = image_array.copy()
            mp_drawing.draw_landmarks(
                debug_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Add prediction text
            cv2.putText(
                debug_image,
                f"{sign} {confidence:.2%}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Convert to base64
            _, buffer = cv2.imencode('.jpg', cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR))
            result['annotated_image'] = f'data:image/jpeg;base64,{base64.b64encode(buffer).decode()}'

        return jsonify(result)

    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return jsonify({
            'error': str(e),
            'debug_info': 'Exception occurred during processing'
        }), 500
