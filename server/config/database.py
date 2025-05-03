from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Make these global variables
client = None
db = None
users = None
scores = None

def init_db():
    global client, db, users, scores
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'asl_detection')

    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        
        # Test the connection
        client.admin.command('ping')
        
        # Get database
        db = client[DB_NAME]
        
        # Initialize collections
        users = db.users
        scores = db.scores
        
        # Create indexes
        users.create_index('username', unique=True)
        users.create_index('email', unique=True)
        
        print("Database connected successfully!")
        
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e

# Initialize database when module is imported
init_db()

def get_db():
    global db
    if db is None:
        init_db()
    return db

def get_users_collection():
    global users
    if users is None:
        init_db()
    return users

def get_scores_collection():
    global scores
    if scores is None:
        init_db()
    return scores