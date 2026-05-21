import os
import psycopg


class DBConnect:

    def __init__(self):
        self.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        print("DB_HOST =", os.environ.get("DB_HOST"))
        print("DB_NAME =", os.environ.get("DB_NAME"))
        print("DB_USER =", os.environ.get("DB_USER"))
        print("Connected to DB successfully")

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
