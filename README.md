# HandSpeak/DetectSIGN: Real-time ASL Recognition & Learning Platform

A full-stack web application that uses machine learning to detect and interpret American Sign Language (ASL) in real-time, providing an interactive learning experience.

## Features

- 🎥 Real-time ASL detection using webcam
- 📚 Interactive learning environment
- 🎮 Gamified spelling practice
- 👤 User authentication and progress tracking
- 🌙 Dark/Light mode support
- 📊 Performance analytics

## Tech Stack

- **Frontend**: React, TypeScript, TailwindCSS
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
   git clone [(https://github.com/folusho-adeyemi/DetectSIGN)]
   cd DetectSIGN
   ```

2. **Frontend Setup**
   ```bash
   cd client
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
   cd client
   npm start
   ```

3. **Access the Application**
   - Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
HandSpeak/
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── context/       # React context providers
│   │   ├── types/         # TypeScript type definitions
│   │   └── utils/         # Utility functions
│   └── public/            # Static assets
│
├── server/                # Backend Python application
│   ├── models/           # ML model and data processing
│   ├── routes/           # API endpoints
│   ├── utils/            # Utility functions
│   └── app.py            # Main application file
│
└── README.md             # Project documentation
```

## Usage

1. **Sign Up/Login**
   - Create an account or login to track your progress
   - Access personalized learning dashboard

2. **Real-time Detection**
   - Allow camera access
   - Position your hand in the frame
   - See real-time ASL letter detection

3. **Learning Mode**
   - Practice individual letters
   - Get immediate feedback
   - Track your accuracy

4. **Game Mode**
   - Spell words using ASL
   - Earn points for correct signs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- MediaPipe for hand tracking
- TensorFlow for machine learning capabilities
- React and TypeScript communities

## Contact

[Folusho Adeyemi] - [Folushovictoradeyemi@gmail.com]

Project Link: [https://github.com/folusho-adeyemi/DetectSIGN](https://github.com/folusho-adeyemi/DetectSIGN)
