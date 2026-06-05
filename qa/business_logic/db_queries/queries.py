from qa.core.db.db_client import DBClient


def clean_db_tables(tables):
    db_client = DBClient()
    cursor = db_client.cursor

    for table in tables:
        cursor.execute(f"DELETE from {table};")
        db_client.connection.commit()

    db_client.close()


def get_cottage_info():
    db_client = DBClient()
    cursor = db_client.cursor
    cursor.execute("""
                       SELECT * FROM cottage_info;
                   """)
    cottage = cursor.fetchone()
    db_client.close()

    return cottage


def add_cottage_to_db(cottage_details):
    db_client = DBClient()
    cursor = db_client.cursor

    cursor.execute("""
                INSERT INTO cottage_info
                (nickname, nightly_rate, capacity, status)
                VALUES (%s, %s, %s, %s)
                RETURNING cottage_id, nickname, nightly_rate, capacity, status;
            """, cottage_details)

    new_cottage = cursor.fetchone()
    db_client.connection.commit()
    db_client.close()

    return new_cottage
