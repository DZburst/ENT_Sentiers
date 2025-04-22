from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = '/data/subjects.json'

def insert_subjects():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for subject in data:
        name = subject['_name']

        cursor.execute(
            "SELECT 1 FROM SUBJECTS WHERE _name = ?",
            (name,)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO SUBJECTS (_name)
                VALUES (?)
                """,
                (name,)
            )
            print(f"Inserted subject: {name}")
        else:
            print(f"Skipped existing subject: {name}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_subjects()