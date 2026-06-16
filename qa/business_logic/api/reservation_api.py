from pydantic import BaseModel


class ReservationAPI:

    def __init__(self, api_client):
        self.api_client = api_client
        self.get_booking_endpoint = api_client.config["get_reservation_endpoint"]
        self.add_booking_endpoint = api_client.config["add_reservation_endpoint"]
        self.check_availability_endpoint = api_client.config["check_availability_endpoint"]

    def get_reservation(self, booking_id):
        booking = self.api_client.call_api_with_retry(f'{self.get_booking_endpoint}/{booking_id}',
                                                      'GET')
        return booking

    def add_reservation(self, reservation_details):
        booking = self.api_client.call_api_with_retry(f'{self.add_booking_endpoint}',
                                                      'POST', json=reservation_details)
        return booking

    def check_availability(self, params):
        availability = self.api_client.call_api_with_retry(f'{self.check_availability_endpoint}',
                                                      'GET', params=params)
        return availability


class BookingResponse(BaseModel):
    booking_id: int
    full_name: str
    email: str
    checkin_date: str
    checkout_date: str
    number_of_guests: str
    special_requests: str
    total_price: float
    status: str
