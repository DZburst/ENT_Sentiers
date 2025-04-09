from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/pupils/backend/data/homeworks.json'

def insert_homeworks():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for homework in data:
        class_id = homework['_class_id']
        
        # Check how many homeworks exist for this class
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

        if len(existing_homeworks) < 2:
            # If fewer than 2 homeworks, insert the new one
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
            # If 2 homeworks already exist, delete the oldest (earliest _issued_at)
            oldest_homework_id = existing_homeworks[-1][0]  # Last one after sorting DESC
            cursor.execute(
                """
                DELETE FROM HOMEWORKS 
                WHERE _id = ?
                """,
                (oldest_homework_id,)
            )
            print(f"Deleted oldest homework for Class {class_id}: ID {oldest_homework_id}")

            # Insert the new homework
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

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_homeworks()