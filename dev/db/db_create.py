import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv

file_path = Path(__file__).parent.parent.parent / "test.env"
load_dotenv(file_path)


def create_db():
    try:
        # Connect to the default database (e.g. 'postgres')
        with psycopg.connect(
                host=os.environ.get('DB_HOST'),
                dbname=os.environ.get('DB_NAME_DEFAULT'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                port=os.environ.get('DB_PORT')
        ) as conn:
            # Enable autocommit mode
            conn.autocommit = True

            with conn.cursor() as cur:
                db_name = os.environ.get('DB_NAME')
                cur.execute(f"CREATE DATABASE {db_name};")
                print("Database created successfully!")

    except psycopg.Error as e:
        print(f"Duplicate DB: {e}")


def create_table():
    # Connect to your target database
    with psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
    ) as conn:
        conn.autocommit = True  # Apply changes immediately (no explicit commit needed)

        with conn.cursor() as cur:
            # booking table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS booking (
                    booking_id SERIAL PRIMARY KEY,
                    full_name VARCHAR(250) NOT NULL,
                    email VARCHAR(50) NOT NULL,
                    checkin_date VARCHAR(10) NOT NULL,
                    checkout_date VARCHAR(10) NOT NULL,
                    number_of_guests VARCHAR(3) NOT NULL,
                    special_requests TEXT,
                    total_price NUMERIC(12,2) NOT NULL,
                    status VARCHAR(20) NOT NULL
                );
            """)

            # cottage info table
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS cottage_info (
                                cottage_id SERIAL PRIMARY KEY,
                                nickname VARCHAR(250) NOT NULL,
                                nightly_rate NUMERIC(12,2) NOT NULL,
                                capacity VARCHAR(3) NOT NULL,
                                status VARCHAR(20) NOT NULL
                            );
                        """)

            # reservation_dates table
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS reservation_dates (
                        booking_id INTEGER,
                        date VARCHAR(10) NOT NULL
                            );
                        """)

        print("✅ Tables created successfully!")
