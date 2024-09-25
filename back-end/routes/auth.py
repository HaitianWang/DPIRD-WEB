import logging
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
   
    if not username or not pwd:
        return jsonify({"status": "0", "message": "Username and password are required"})

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        if cursor.fetchone():
            return jsonify({"status": "0", "message": "Username already exists"})
   
        # Hash the password
        hashed_password = generate_password_hash(pwd)
   
        # Insert new user
        cursor.execute("INSERT INTO user (username, pwd) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        
        return jsonify({"status": "1", "message": "Registration successful"})
    
    except Exception as e:
        conn.rollback()
        logging.error(f"Registration failed: {str(e)}")
        return jsonify({"status": "0", "message": "Registration failed due to an error"})
    
    finally:
        cursor.close()
        conn.close()


@auth_bp.route('/update_password', methods=['POST'])
def update_password():
    print("Received a request to update password")
    username = request.form.get("username")
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    print("username:", username)
    print("current_password:", current_password)
    print("new_password:", new_password)

    if not username or not current_password or not new_password:
        return jsonify({"status": "0", "message": "Username, current password, and new password are required"})

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Retrieve the user from the database
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"status": "0", "message": "User does not exist"})

        # Check if the current password matches the stored password
        if not check_password_hash(user['pwd'], current_password):
            return jsonify({"status": "0", "message": "Current password is incorrect"})

        # Hash the new password
        hashed_new_password = generate_password_hash(new_password)

        # Update the password in the database
        cursor.execute("UPDATE user SET pwd = ? WHERE username = ?", (hashed_new_password, username))
        conn.commit()

        return jsonify({"status": "1", "message": "Password updated successfully"})

    except sqlite3.Error as e:
        conn.rollback()
        logging.error(f"Password update failed: {str(e)}")
        return jsonify({"status": "0", "message": "Password update failed due to a database error"})

    finally:
        cursor.close()
        conn.close()
