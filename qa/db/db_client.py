import os
import psycopg


class DBClient:

    def __init__(self):
        self.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        self.host = os.getenv("DB_HOST")

        if not self.host:
            raise ValueError("DB_HOST is empty. Check your environment variables!")

        self.cursor = self.connection.cursor()

    def commit(self):
        """Commit current transaction"""
        self.connection.commit()

    def close(self):
        """Close cursor and connection"""
        self.cursor.close()
        self.connection.close()

    def clean_db_tables(self, tables):
        cursor = self.cursor

        for table in tables:
            cursor.execute(f"DELETE from {table};")
            self.connection.commit()


    def get_cottage_info(self):
        cursor = self.cursor
        cursor.execute("""
                           SELECT * FROM cottage_info;
                       """)
        cottage = cursor.fetchone()

        return cottage

    def add_cottage_to_db(self, cottage_details):
        cursor = self.cursor

        cursor.execute("""
                    INSERT INTO cottage_info
                    (nickname, nightly_rate, capacity, status)
                    VALUES (%s, %s, %s, %s)
                    RETURNING cottage_id, nickname, nightly_rate, capacity, status;
                """, cottage_details)

        new_cottage = cursor.fetchone()
        self.connection.commit()

        return new_cottage

