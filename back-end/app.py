from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from tensorflow.keras.models import load_model
import tensorflow as tf
import logging as rel_log
import os
import sqlite3
from custom_layers import custom_objects
from routes.main import main_bp
from routes.auth import auth_bp
from routes.file_operations import file_ops_bp

# Configuration
UPLOAD_FOLDER = r'./uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'tif', 'zip'}

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # CORS for all routes

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-should-change-this'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # Logging
    werkzeug_logger = rel_log.getLogger('werkzeug')
    werkzeug_logger.setLevel(rel_log.ERROR)

    # Database
    init_db()

    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(file_ops_bp)

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
        return response

    return app

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pwd TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app = create_app()

    # Ensure required directories exist
    for directory in ['uploads', 'tmp/ct', 'tmp/draw', 'tmp/image', 'tmp/mask', 'tmp/uploads']:
        os.makedirs(directory, exist_ok=True)

    with app.app_context():
        custom_objects['mse'] = tf.keras.losses.mse
        app.model = load_model('cnn_model_with_l1.h5', custom_objects=custom_objects)

    app.run(host='127.0.0.1', port=5003, debug=True)
