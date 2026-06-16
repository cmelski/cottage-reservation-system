import os
import psycopg
from qa.core.utils.logging_utils import get_logger
logger = get_logger(__name__)


class DBClient:

    def __init__(self, trace_id: str = None):
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

        if trace_id:
            self.trace_id = trace_id
            logger.info(f'TRACE={self.trace_id}')

    def commit(self):
        """Commit current transaction"""
        self.connection.commit()

    def close(self):
        """Close cursor and connection"""
        self.cursor.close()
        self.connection.close()

    def reset_db_tables(self, tables):

        cursor = self.cursor
        for table in tables:
            cursor.execute(f"DELETE from {table};")
            self.commit()



