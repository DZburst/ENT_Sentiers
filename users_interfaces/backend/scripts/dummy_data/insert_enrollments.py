from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/backend/data/enrollments.json'

def insert_enrollments():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for enrollment in data:
        student_id = enrollment['_student_id']
        class_id = enrollment['_class_id']

        cursor.execute(
            "SELECT 1 FROM ENROLLMENTS WHERE _student_id = ? AND _class_id = ?",
            (student_id, class_id)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO ENROLLMENTS (_student_id, _class_id, _enrolled_at)
                VALUES (?, ?, ?)
                """,
                (student_id, class_id, enrollment['_enrolled_at'])
            )
            print(f"Inserted enrollment: Student {student_id} in Class {class_id}")
        else:
            print(f"Skipped existing enrollment: Student {student_id} in Class {class_id}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_enrollments()