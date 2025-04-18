from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/backend/data/classes.json'

def insert_classes():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for cls in data:
        cursor.execute(
            """
            SELECT 1 FROM CLASSES 
            WHERE _subject_id = ? AND _teacher_id = ? AND _day_of_week = ? AND _start_time = ?
            """,
            (cls['_subject_id'], cls['_teacher_id'], cls['_day_of_week'], cls['_start_time'])
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO CLASSES (
                    _subject_id, _teacher_id, _level, _classroom_id, 
                    _start_time, _end_time, _day_of_week, _is_online
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cls['_subject_id'],
                    cls['_teacher_id'],
                    cls['_level'],
                    cls['_classroom_id'],
                    cls['_start_time'],
                    cls['_end_time'],
                    cls['_day_of_week'],
                    cls['_is_online']
                )
            )
            print(f"Inserted class: Subject {cls['_subject_id']} on {cls['_day_of_week']} at {cls['_start_time']}")
        else:
            print(f"Skipped existing class: Subject {cls['_subject_id']} on {cls['_day_of_week']} at {cls['_start_time']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_classes()