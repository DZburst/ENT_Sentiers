from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = '/data/homeworks.json'

def insert_homeworks():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for homework in data:
        class_id = homework['_class_id']
        
        cursor.execute(
            """
            SELECT _id, _issued_at 
            FROM HOMEWORKS 
            WHERE _class_id = ? 
            ORDER BY _issued_at DESC
            """,
            (class_id,)
        )
        existing_homeworks = cursor.fetchall()

        cursor.execute(
            """
            SELECT 1
            FROM HOMEWORKS
            WHERE _class_id = ? AND _issued_at = ?
            """,
            (class_id, homework['_issued_at'])
        )
        already_exists = cursor.fetchone()

        if not already_exists:
            if len(existing_homeworks) < 2:
                cursor.execute(
                    """
                    INSERT INTO HOMEWORKS (_class_id, _description, _issued_at)
                    VALUES (?, ?, ?)
                    """,
                    (
                        class_id,
                        homework['_description'],
                        homework['_issued_at']
                    )
                )
                print(f"Inserted homework: Class {class_id} issued on {homework['_issued_at']}")
            else:
                oldest_homework_id = existing_homeworks[-1][0]
                cursor.execute(
                    """
                    DELETE FROM HOMEWORKS 
                    WHERE _id = ?
                    """,
                    (oldest_homework_id,)
                )
                print(f"Deleted oldest homework for Class {class_id}: ID {oldest_homework_id}")

                cursor.execute(
                    """
                    INSERT INTO HOMEWORKS (_class_id, _description, _issued_at)
                    VALUES (?, ?, ?)
                    """,
                    (
                        class_id,
                        homework['_description'],
                        homework['_issued_at']
                    )
                )
                print(f"Inserted homework: Class {class_id} issued on {homework['_issued_at']}")
        else:
            print(f"Skipped existing homework: Class {class_id} issued on {homework['_issued_at']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_homeworks()