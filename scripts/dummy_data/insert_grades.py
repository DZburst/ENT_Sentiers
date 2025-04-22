from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = '/data/grades.json'

def insert_grades():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for grade in data:
        cursor.execute(
            """
            SELECT 1 FROM GRADES 
            WHERE _student_id = ? AND _subject_id = ? AND _date = ?
            """,
            (grade['_student_id'], grade['_subject_id'], grade['_date'])
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO GRADES (_student_id, _subject_id, _grade, _date, _comment)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    grade['_student_id'],
                    grade['_subject_id'],
                    grade['_grade'],
                    grade['_date'],
                    grade.get('_comment')
                )
            )
            print(f"Inserted grade: Student {grade['_student_id']} in Subject {grade['_subject_id']} on {grade['_date']}")
        else:
            print(f"Skipped existing grade: Student {grade['_student_id']} in Subject {grade['_subject_id']} on {grade['_date']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_grades()