from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/backend/data/teaches.json'

def insert_teaches():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for teach in data:
        teacher_id = teach['_teacher_id']
        subject_id = teach['_subject_id']

        cursor.execute(
            "SELECT 1 FROM TEACHES WHERE _teacher_id = ? AND _subject_id = ?",
            (teacher_id, subject_id)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO TEACHES (_teacher_id, _subject_id)
                VALUES (?, ?)
                """,
                (teacher_id, subject_id)
            )
            print(f"Inserted teach relationship: Teacher {teacher_id} teaches Subject {subject_id}")
        else:
            print(f"Skipped existing teach relationship: Teacher {teacher_id} teaches Subject {subject_id}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_teaches()