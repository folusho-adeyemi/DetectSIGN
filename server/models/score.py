from datetime import datetime
from bson import ObjectId

class Score:
    def __init__(self, user_id, score, word=None):
        self.user_id = user_id
        self.score = score
        self.word = word
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'score': self.score,
            'word': self.word,
            'created_at': self.created_at
        } 