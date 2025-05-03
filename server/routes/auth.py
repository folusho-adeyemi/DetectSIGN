from flask import Blueprint, request, jsonify
from services.user_service import UserService
from utils.jwt import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        user = UserService.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        
        token = create_access_token(str(user['_id']))
        
        return jsonify({
            'token': token,
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = UserService.get_user_by_username(data['username'])
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        user_id = str(user._id) if user._id else None
        if not user_id:
            return jsonify({'error': 'User ID not found'}), 500
        
        token = create_access_token(user_id)
        
        return jsonify({
            'token': token,
            'user': {
                'id': user_id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500 