# This script configures and runs a Flask web application for the DPIRD Intellicrop project.
# The main features include:
# 1. CORS (Cross-Origin Resource Sharing) support to allow requests from different origins.
# 2. Session management and security settings such as session timeout, HTTP-only cookies, and secret keys.
# 3. Registration of blueprints for handling different routes (main, authentication, and file operations).
# 4. Initialization of an SQLite database for user management (username and hashed password storage).
# 5. Loading a pre-trained TensorFlow model for processing with custom layers.


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

# Configuration settings for the DPIRD Intellicrop project
UPLOAD_FOLDER = r'./uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'tif', 'zip'}

def create_app():
    """
    Creates and configures the Flask application, including CORS settings, secret keys, and session configurations.
    Registers blueprints for main, auth, and file operations routes.

    Returns:
    Flask app object: Configured Flask app ready to run.
    """
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

    # Initialize the database
    init_db()

    # Register blueprints for various routes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(file_ops_bp)

    @app.after_request
    def after_request(response):
        """
        Adds necessary headers for CORS and credentials after each request.

        Parameters:
        response (Response object): The Flask response object.

        Returns:
        Response object: Modified response with added headers.
        """
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
        return response

    return app

def init_db():
    """
    Initializes the SQLite database by creating the 'user' table if it does not already exist.
    The table contains user information including id, username, and hashed password.
    """
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
    # Create the Flask app
    app = create_app()

    # Ensure the necessary directories exist
    for directory in ['uploads', 'tmp/ct', 'tmp/draw', 'tmp/image', 'tmp/mask', 'tmp/uploads']:
        os.makedirs(directory, exist_ok=True)

    # Load the TensorFlow model with custom layers
    with app.app_context():
        custom_objects['mse'] = tf.keras.losses.mse  # Adding custom loss function
        app.model = load_model('model1.h5', custom_objects=custom_objects)  # Load pre-trained model

    # Run the Flask app on localhost at port 5003
    app.run(host='127.0.0.1', port=5003, debug=True)
