from flask import Blueprint, jsonify, request
import sqlite3
import db
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    pwd = request.form.get("pwd")
    
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['pwd'], pwd):
            return jsonify({"status": "1", "message": "Login successful"})
        else:
            return jsonify({"status": "0", "message": "Invalid username or password"})
    except sqlite3.Error as e:
        return jsonify({"status": "0", "message": "Login failed due to database error"})
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/regi', methods=['POST'])
def regi():
    username = request.form.get("username")
    pwd = request.form.get("pwd")
   
    # Check if user exists
    exists = db.query_db("SELECT * FROM user WHERE username = ?", (username,), one=True)
    if exists:
        return jsonify({"status": "0", "message": "Username already exists"})
   
    # Hash the password
    hashed_password = generate_password_hash(pwd)
   
    # Insert new user
    conn = db.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user (username, pwd) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return jsonify({"status": "1", "message": "Registration successful"})
    except sqlite3.Error as e:
        return jsonify({"status": "0", "message": "Registration failed due to database error"})
    finally:
        cursor.close()
        conn.close()