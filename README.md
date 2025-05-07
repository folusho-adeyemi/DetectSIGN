# HandSpeak/DetectSIGN: Real-time ASL Recognition & Learning Platform
A full-stack web application for real-time American Sign Language (ASL) detection, interpretation, and learning.

## Features

-  Real-time ASL detection using webcam
-  Interactive learning environment
-  Gamified spelling practice with ASL
-  User authentication and progress tracking
-  Dark/Light mode toggle
-  Performance tracking and statistics

## Tech Stack

- **Frontend**: React, TypeScript, CSS
- **Backend**: Python Flask, TensorFlow
- **Database**: MongoDB
- **Computer Vision**: MediaPipe
- **Authentication**: JWT

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB
- Webcam

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DETECT_SIGN.git
   cd DETECT_SIGN
   ```

2. **Frontend Setup**
   ```bash
   npm install
   ```

3. **Backend Setup**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Create `.env` file in server directory:
     ```
     MONGODB_URI=your_mongodb_uri
     JWT_SECRET=your_jwt_secret
     PORT=5000
     ```

## Running the Application

1. **Start the Backend Server**
   ```bash
   cd server
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python app.py
   ```

2. **Start the Frontend Development Server**
   ```bash
   npm start
   ```

3. **Access the Application**
   - Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
DETECT_SIGN/
├── public/                 # Static assets
├── src/                    # Frontend React application
│   ├── components/         # React components
│   │   ├── AuthPage/       # Authentication components
│   │   ├── CameraFeed/     # Webcam input
│   │   ├── SignDisplay/    # Sign detection display
│   │   ├── SpellingGame/   # Game components
│   │   ├── ThemeToggle/    # Dark/Light mode
│   │   └── WelcomeSection/ # User welcome
│   ├── context/            # React context providers
│   ├── services/           # API services
│   ├── styles/             # CSS files
│   └── App.tsx             # Main application
│
├── server/                 # Backend Python application
│   ├── models/             # ML model and data schema
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── collect_data.py     # Data collection script
│   ├── train_model.py      # Model training script
│   └── app.py              # Main server file
│
└── README.md               # Project documentation
```

## Usage

1. **Sign Up/Login**
   - Create an account or login to track your progress
   - Access your personalized dashboard

2. **Real-time Detection**
   - Allow camera access
   - Position your hand in the frame
   - See real-time ASL letter detection

3. **Learning Mode**
   - Practice individual letters
   - Get immediate feedback on your signs
   - Track your accuracy over time

4. **Game Mode**
   - Spell words using ASL signs
   - Challenge yourself with different difficulty levels
   - Earn points for correct signs

## Model Training

If you want to improve the model's accuracy:

1. Run the data collection script:
   ```bash
   cd server
   python collect_data.py
   ```
   - Follow the prompts to capture hand signs for each letter
   - The script will guide you through the collection process
   - Data will be saved in the `collected_data` directory

2. Train the model with your new data:
   ```bash
   python train_model.py
   ```
   - The script uses early stopping and learning rate reduction
   - Model checkpoints are saved during training
   - The best model will be saved as `asl_model.h5`

3. Test the model before deploying:
   ```bash
   python test_model.py
   ```

## ML Model Architecture

Our ASL detection system uses a Convolutional Neural Network (CNN) approach with MediaPipe hand landmarks as input features:

### Data Processing Pipeline
1. **Hand Detection**: Using MediaPipe to extract 21 hand landmarks (x, y, z coordinates)
2. **Feature Engineering**: Converting raw landmarks into distance-based features
3. **Normalization**: Scaling features to improve model generalization

### Model Architecture
- **Input Layer**: Flattened hand landmark coordinates (63 features)
- **Hidden Layers**: Dense layers with dropout for regularization
- **Output Layer**: 26 units (one for each ASL letter) with softmax activation

### Why This Approach?
I chose this approach for several reasons:
- **Efficiency**: Landmark-based detection is computationally lighter than image-based CNNs
- **Accuracy**: Achieves 85%+ accuracy with relatively small training data
- **Real-time Performance**: Low latency (<300ms) makes it suitable for interactive applications
- **Personalization**: The system allows users to train with their own data, improving accuracy for individual users

### Limitations and Improvements
- Currently only detects static hand signs (letters)
- Future work could include dynamic gesture recognition
- Transfer learning from larger ASL datasets could improve accuracy

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- MediaPipe for hand tracking capabilities
- TensorFlow for machine learning functionality
- MongoDB for database solutions
- React and TypeScript communities

## Contact

[Folusho Adeyemi] - [Folushovictoradeyemi@gmail.com]

Project Link: [https://github.com/folusho-adeyemi/DetectSIGN](https://github.com/folusho-adeyemi/DetectSIGN)
