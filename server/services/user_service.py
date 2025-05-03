from models.user import User
from config.database import get_users_collection
from bson import ObjectId
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(username, email, password):
        users = get_users_collection()
        
        # Check if user exists
        if users.find_one({'$or': [{'username': username}, {'email': email}]}):
            raise ValueError('Username or email already exists')

        user = User(username, email, password)
        result = users.insert_one(user.to_dict())
        user_dict = user.to_dict()
        user_dict['_id'] = result.inserted_id
        return user_dict

    @staticmethod
    def get_user_by_username(username):
        users = get_users_collection()
        user_data = users.find_one({'username': username})
        if user_data:
            return User.from_dict(user_data)
        return None

    @staticmethod
    def add_score(user_id, score, word=None):
        users = get_users_collection()
        users.update_one(
            {'_id': ObjectId(user_id)},
            {'$push': {'scores': {
                'score': score,
                'word': word,
                'created_at': datetime.utcnow()
            }}}
        )

    @staticmethod
    def get_user_scores(user_id):
        users = get_users_collection()
        user = users.find_one({'_id': ObjectId(user_id)})
        return user.get('scores', []) if user else [] 