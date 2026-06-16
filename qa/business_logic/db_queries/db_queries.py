

def get_cottage_info(db_client):
    cursor = db_client.cursor
    cursor.execute("""
                       SELECT * FROM cottage_info;
                   """)
    cottage = cursor.fetchone()

    return cottage


def add_cottage_to_db(cottage_details, db_client):
    cursor = db_client.cursor

    cursor.execute("""
                INSERT INTO cottage_info
                (nickname, nightly_rate, capacity, status)
                VALUES (%s, %s, %s, %s)
                RETURNING cottage_id, nickname, nightly_rate, capacity, status;
            """, cottage_details)

    new_cottage = cursor.fetchone()
    db_client.connection.commit()

    return new_cottage


def add_booking_to_db(booking_details, db_client):
    cursor = db_client.cursor
    cursor.execute("""
                SELECT setval(
                    pg_get_serial_sequence('booking', 'booking_id'),
                (SELECT MAX(booking_id) FROM booking)
                );
                """)
    db_client.connection.commit()

    cursor.execute("""
            INSERT INTO booking
            (full_name, email, checkin_date, checkout_date, number_of_guests, 
            special_requests, total_price, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING booking_id, full_name, email, checkin_date, checkout_date,
                        number_of_guests, special_requests, total_price, status;
            """, booking_details)

    new_booking = cursor.fetchone()
    db_client.connection.commit()

    return new_booking
