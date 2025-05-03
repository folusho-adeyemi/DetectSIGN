from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    def __init__(self, username, email, password):
        self._id = None
        self.username = username
        self.email = email
        self.password = self._hash_password(password)
        self.created_at = datetime.utcnow()
        self.scores = []

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'scores': self.scores
        }

    @staticmethod
    def from_dict(data):
        user = User(data['username'], data['email'], '')
        user._id = data.get('_id')
        user.password = data['password']  # Already hashed
        user.created_at = data.get('created_at', datetime.utcnow())
        user.scores = data.get('scores', [])
        return user 