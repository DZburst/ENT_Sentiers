from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = 'users_interfaces/pupils/backend/data/news.json'

def insert_news():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for news in data:
        cursor.execute(
            """
            SELECT 1 FROM NEWS 
            WHERE _title = ?
            """,
            (news['_title'],)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO NEWS (_title, _content, _image_url)
                VALUES (?, ?, ?)
                """,
                (
                    news['_title'],
                    news['_content'],
                    news['_image_url']
                )
            )
            print(f"Inserted news: Title {news['_title']}")
        else:
            print(f"Skipped existing news: Title {news['_title']}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_news()