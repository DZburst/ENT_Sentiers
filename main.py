# Import necessary modules from Flask and other libraries
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
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


# ================================== #
# ===== HTML Template Endpoints ==== #
# ================================== #

# Home page
@app.route('/home')
def serve_home():
    return render_template('home.html')

# About page
@app.route('/about')
def serve_about():
    return render_template('about.html')

# Messaging page
@app.route('/messaging')
def serve_messaging():
    return render_template('messaging.html')

# Myspace page
@app.route('/myspace')
def serve_myspace():
    return render_template('myspace.html')

# Login page (for GET requests, to see the form visually)
@app.route('/', methods=['GET'])
def serve_login_page():
    return render_template('login.html')


# ========================== #
# ===== Home Endpoints ===== #
# ========================== #

@app.route('/read_news', methods=['GET'])
def read_news():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM NEWS")
    news_items = cursor.fetchall()
    result = [dict(news_item) for news_item in news_items]
    close_db_connection(conn, cursor)

    return jsonify(result), 200

@app.route('/create_news', methods=['POST'])
def create_news():
    data = request.get_json()
    if not data or not all(key in data for key in ('title', 'content', 'image_url')):
        return jsonify({"error": "Veuillez remplir tous les champs afin d'insérer une nouvelle entrée."}), 400
    
    conn, cursor = get_db_connection()
    cursor.execute("INSERT INTO NEWS (_title, _content, _image_url) VALUES (?, ?, ?)",
                   (data['_title'], data['_content'], data['_image_url']))
    conn.commit()
    close_db_connection(conn, cursor)

    return jsonify({"message": "Nouvelle entrée créée avec succès."}), 201

@app.route('/delete_news', methods=['DELETE'])
def delete_news():
    data = request.get_json()
    if not data or 'news_id' not in data:
        return jsonify({"error": "Veuillez indiquer l'ID de la nouvelle entrée à supprimer."}), 400
    
    news_id = data['news_id']
    conn, cursor = get_db_connection()
    cursor.execute("DELETE FROM NEWS WHERE _id = ?", (news_id,))
    if cursor.rowcount == 0:
        close_db_connection(conn, cursor)
        return jsonify({"error": "Aucune entrée trouvée avec cet ID."}), 404
    
    conn.commit()
    close_db_connection(conn, cursor)

    return jsonify({"message": "Nouvelle entrée supprimée avec succès."}), 200

# =========================== #

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)