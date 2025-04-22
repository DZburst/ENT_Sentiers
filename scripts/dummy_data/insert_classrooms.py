from utils import get_db_connection, close_db_connection, load_json_file

FILE_PATH = '/data/classrooms.json'

def insert_classrooms():
    conn, cursor = get_db_connection()
    
    data = load_json_file(FILE_PATH)
    if not data:
        close_db_connection(conn, cursor)
        return

    for classroom in data:
        name = classroom['_name']
        nb_seats = classroom['_nb_seats']

        cursor.execute(
            "SELECT 1 FROM CLASSROOMS WHERE _name = ?",
            (name,)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO CLASSROOMS (_name, _nb_seats)
                VALUES (?, ?)
                """,
                (name, nb_seats)
            )
            print(f"Inserted classroom: {name}")
        else:
            print(f"Skipped existing classroom: {name}")

    close_db_connection(conn, cursor)

if __name__ == "__main__":
    insert_classrooms()