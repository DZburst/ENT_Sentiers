from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/backend/data/mails.json'

def insert_mails():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for mail in data:
        cursor.execute(
            """
            SELECT 1 FROM MAILS 
            WHERE _sender_id = ? AND _subject = ? AND _sent_at = ?
            """,
            (mail['_sender_id'], mail['_subject'], mail['_sent_at'])
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO MAILS (_sender_id, _subject, _content, _sent_at)
                VALUES (?, ?, ?, ?)
                """,
                (mail['_sender_id'], mail['_subject'], mail['_content'], mail['_sent_at'])
            )
            print(f"Inserted mail: Subject {mail['_subject']} from User {mail['_sender_id']} at {mail['_sent_at']}")
        else:
            print(f"Skipped existing mail: Subject {mail['_subject']} from User {mail['_sender_id']} at {mail['_sent_at']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_mails()