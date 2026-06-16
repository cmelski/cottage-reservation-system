from qa.business_logic.flows.book_cottage_flow import BookCottageFlow
from qa.business_logic.api.reservation_api import ReservationAPI


class ReservationFacade:
    def __init__(self, page, api_client, single_booking_details):
        self.page = page
        self.single_booking_details = single_booking_details
        self.book_cottage_flow = BookCottageFlow(self.page)
        self.reservation_api = ReservationAPI(api_client)

    def create_reservation(self):
        booking_confirmation = self.book_cottage_flow.complete_booking(self.single_booking_details)
        booking_confirmation_details = booking_confirmation.get_confirmation_details()
        booking_id_confirmation_details = booking_confirmation_details['booking_id']
        booking_api_response = self.reservation_api.get_reservation(booking_id_confirmation_details)
        booking_api_data = booking_api_response.json()['booking']
        api_response_data = [
            booking_api_data["full_name"],
            booking_api_data["email"],
            booking_api_data["checkin_date"],
            booking_api_data["checkout_date"],
            booking_api_data["number_of_guests"],
            booking_api_data["special_requests"],
            float(booking_api_data["total_price"]),
            booking_api_data["status"]
        ]

        return booking_confirmation_details, api_response_data
