
class ReservationAPI:

    def __init__(self, api_client):
        self.api_client = api_client
        self.get_booking_endpoint = 'api/get_reservation_by_booking_id'

    def get_reservation(self, booking_id):
        booking = self.api_client.call_api_with_retry(f'{self.get_booking_endpoint}/{booking_id}',
                                                      'GET')
        return booking

