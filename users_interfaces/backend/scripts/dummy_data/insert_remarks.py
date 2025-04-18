from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/backend/data/remarks.json'

def insert_remarks():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for remark in data:
        cursor.execute(
            """
            SELECT 1 FROM REMARKS 
            WHERE _student_id = ? AND _subject_id = ? AND _date = ?
            """,
            (remark['_student_id'], remark['_subject_id'], remark['_date'])
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO REMARKS (_student_id, _subject_id, _date, _content)
                VALUES (?, ?, ?, ?)
                """,
                (
                    remark['_student_id'],
                    remark['_subject_id'],
                    remark['_date'],
                    remark['_content']
                )
            )
            print(f"Inserted remark: Student {remark['_student_id']} in Subject {remark['_subject_id']} on {remark['_date']}")
        else:
            print(f"Skipped existing remark: Student {remark['_student_id']} in Subject {remark['_subject_id']} on {remark['_date']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_remarks()