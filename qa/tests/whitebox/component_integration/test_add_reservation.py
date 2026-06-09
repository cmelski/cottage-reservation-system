"""reset the db using a fixture and test new booking can be created."""
from dev.db.db_client import DBClient
from qa.business_logic.data.new_booking import NewBooking


def test_add_reservation(reset_db):
    """reset the db using a fixture and test new booking can be created."""
    # connect to DB
    db_client = DBClient()

    # add booking using dev function
    new_booking = NewBooking()
    booking_details = new_booking.generate_new_reservation_details()
    new_booking_db = list(db_client.add_booking_to_db(booking_details))
    print(f'Booking details sent: {booking_details}')
    print(f'Booking DB response: {new_booking_db[1:]}')

    # assert new booking in DB matches values sent
    # slice out the ID

    assert new_booking_db[1:] == list(booking_details)
