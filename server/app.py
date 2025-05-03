from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from config.database import init_db
import model

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize database
    init_db()

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Register routes from model.py
    @app.route('/detect', methods=['POST'])
    def detect():
        return model.detect()

    return app

app = create_app()

if __name__ == '__main__':
    print("Starting server...")
    app.run(port=3001, debug=True) 