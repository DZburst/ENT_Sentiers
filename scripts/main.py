# Import necessary modules from Flask and other libraries
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
import sqlite3
from datetime import timedelta
from utils import get_db_connection, close_db_connection
from dotenv import load_dotenv
import bcrypt
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
app.secret_key = os.getenv('FLASK_SECRET_KEY')
# Configure session settings (e.g., session lifetime)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Sessions last 1 hour

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# =========================== #
# ===== Login Endpoints ===== #
# =========================== #

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username') if data else None
    plain_password = data.get('password') if data else None
    role = data.get('role') if data else None
    
    if not data or not username or not plain_password or not role:
        return jsonify({'error': 'Missing credentials'}), 400

    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM USERS WHERE _username = ?", (username,))
    user = cursor.fetchone()
    
    if user is None or not bcrypt.checkpw(plain_password.encode('utf_8'), user['_password_hash']):
        close_db_connection(conn, cursor)
        return jsonify({'error': 'Invalid credentials'}), 401

    if user['_role'] != role:
        close_db_connection(conn, cursor)
        return jsonify({'error': 'Selected role does not match user role'}), 401

    session['user_id'] = user['_id']
    session['role'] = user['_role']
    close_db_connection(conn, cursor)

    return jsonify({'message': 'Login successful', 'user_id': user['_id'], 'role': user['_role']}), 200
    


# ========================== #
# ===== Home Endpoints ===== #
# ========================== #

@app.route('/api/news', methods=['GET'])
def news():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NEWS")
    data = cursor.fetchall()
    result = [dict(row) for row in data]
    conn.close()

    return jsonify(result), 200

    
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)