from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/pupils/backend/data/users.json'

def insert_users():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for user in data:
        password_hash = user['_password_hash']

        cursor.execute(
            "SELECT 1 FROM USERS WHERE _password_hash = ?",
            (password_hash,)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO USERS (
                    _created_at, _active, _name, _surname, _age, _username, 
                    _password_hash, _profile_pic, _email, _phone, _role, 
                    _parent_name, _parent_email, _parent_phone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user['_created_at'],
                    user['_active'],
                    user['_name'],
                    user['_surname'],
                    user['_age'],
                    user['_username'],
                    user['_password_hash'],
                    user['_profile_pic'],
                    user['_email'],
                    user['_phone'],
                    user['_role'],
                    user['_parent_name'],
                    user['_parent_email'],
                    user['_parent_phone']
                )
            )
            print(f"Inserted user: {user['_username']}")
        else:
            print(f"Skipped existing user: {user['_username']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_users()