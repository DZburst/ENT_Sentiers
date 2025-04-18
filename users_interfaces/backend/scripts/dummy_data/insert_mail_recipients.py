from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/backend/data/mail_recipients.json'

def insert_mail_recipients():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for recipient in data:
        cursor.execute(
            """
            SELECT 1 FROM MAIL_RECIPIENTS 
            WHERE _mail_id = ? AND _receiver_id = ?
            """,
            (recipient['_mail_id'], recipient['_receiver_id'])
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO MAIL_RECIPIENTS (_mail_id, _receiver_id, _is_read, _folder)
                VALUES (?, ?, ?, ?)
                """,
                (recipient['_mail_id'], recipient['_receiver_id'], recipient['_is_read'], recipient['_folder'])
            )
            print(f"Inserted mail recipient: Mail {recipient['_mail_id']} to User {recipient['_receiver_id']}")
        else:
            print(f"Skipped existing mail recipient: Mail {recipient['_mail_id']} to User {recipient['_receiver_id']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_mail_recipients()