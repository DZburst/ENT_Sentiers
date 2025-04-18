import sqlite3
import bcrypt
from utils import get_db_connection, close_db_connection

def hash_existing_passwords():
    conn, cursor = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT _id, _password_hash FROM USERS")
    users = cursor.fetchall()

    for user in users:
        user_id = user["_id"]
        plain_password = user["_password_hash"]
        hashed_password = bcrypt.hashpw(plain_password.encode('utf_8'), bcrypt.gensalt())
        cursor.execute("UPDATE USERS SET _password_hash = ? WHERE _id = ?", (hashed_password, user_id))
    
    close_db_connection(conn, cursor)

if __name__ == "__main__":
    hash_existing_passwords()
