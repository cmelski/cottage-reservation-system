
def convert_booking_details_tuple_to_dictionary(tuple_data):
    new_dict = dict(zip(
        ["full_name", "email", "checkin", "checkout", "number_of_guests",
         "special_requests", "price", "status"],
        tuple_data
    ))

    return new_dict
