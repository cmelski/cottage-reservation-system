from dev.db.db_connect import DBConnect
from dev.utils.generic_utils import check_availability, get_reservation_dates
from datetime import timedelta
from datetime import datetime

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

    def get_reservation_dates_from_db(self):
        cursor = self.connection.cursor
        cursor.execute("""
                        SELECT * FROM reservation_dates;
                        """)
        reservation_dates = cursor.fetchall()

        return reservation_dates

    def add_booking_to_db(self, booking_details):
        existing_reservation_dates = self.get_reservation_dates_from_db()
        reservation_dates = [reservation_date[1] for reservation_date
                             in existing_reservation_dates]

        checkin = booking_details[2]
        checkout = booking_details[3]

        available = check_availability(checkin, checkout, reservation_dates)
        if len(available) == 0:  # create booking as reservation dates don't conflict with existing dates
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
            booking_id = new_booking[0]
            booking_dates = get_reservation_dates(checkin, checkout)

            self.add_reservation_dates_to_db(booking_dates, booking_id)

            return new_booking
        else:
            return available

    def add_reservation_dates_to_db(self, dates, booking_id):
        cursor = self.connection.cursor
        for date in dates:
            cursor.execute("""
                INSERT INTO reservation_dates
                (booking_id, date)
                VALUES (%s, %s);
            """, (booking_id, date))

        self.connection.commit()

    def get_booking(self, booking_id):
        cursor = self.connection.cursor
        cursor.execute("""
                          SELECT * FROM booking
                          WHERE booking_id = %s;
                          """, (booking_id,))  # <-- pass as tuple
        booking = cursor.fetchone()
        return booking

    def get_availability(self, checkin, checkout):

        cursor = self.connection.cursor
        print(checkin, checkout)

        cursor.execute("""
            SELECT date
            FROM reservation_dates
            WHERE date::date >= %s
            AND date::date < %s;
        """, (checkin, checkout))

        rows = cursor.fetchall()

        booked_dates = {
            datetime.strptime(row[0], "%Y-%m-%d").date()
            for row in rows
        }

        availability = []

        current = checkin

        while current < checkout:
            availability.append({
                "date": current.isoformat(),
                "available": current not in booked_dates
            })

            current += timedelta(days=1)

        return availability
