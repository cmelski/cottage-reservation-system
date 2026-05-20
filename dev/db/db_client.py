from dev.db.db_connect import DBConnect


class DBClient:

    def __init__(self):
        self.connection = DBConnect()

    def get_cottage_info_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("""
                      SELECT * FROM cottage_info;
                      """)
        cottage_info = cursor.fetchone()

        return cottage_info

    def add_booking_to_db(self, booking_details):
        cursor = self.connection.cursor
        cursor.execute("""
                SELECT setval(
                  pg_get_serial_sequence('booking', 'booking_id'),
                (SELECT MAX(booking_id) FROM booking)
                );
                """)
        self.connection.commit()

        cursor.execute("""
            INSERT INTO booking
            (full_name, email, checkin_date, checkout_date, number_of_guests, 
            special_requests, total_price, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING booking_id, full_name, email, checkin_date, checkout_date,
                      number_of_guests, special_requests, total_price, status;
        """, booking_details)

        new_booking = cursor.fetchone()
        self.connection.commit()
        return new_booking
