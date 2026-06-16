from faker import Faker
from datetime import timedelta
import random

fake = Faker('en_GB')
PRICE_PER_NIGHT = 300.00
LENGTH_OF_STAY = 3


class NewBooking:
    def __init__(self):
        self.checkin = fake.future_date()

    def generate_new_reservation_details(self) -> tuple:
        full_name = fake.name()
        email = fake.email()
        checkin_date = self.checkin
        checkout_date = checkin_date + timedelta(days=LENGTH_OF_STAY)
        price = PRICE_PER_NIGHT * LENGTH_OF_STAY
        status = 'confirmed'
        number_of_guests_choices = ['1', '2', '3', '4', '5+']
        number_of_guests = random.choice(number_of_guests_choices)
        special_requests = fake.sentence()
        self.update_checkin_date(checkout_date)
        data = (full_name, email, checkin_date.isoformat(), checkout_date.isoformat(),
                number_of_guests, special_requests, price, status)
        return data

    def update_checkin_date(self, checkout_date):
        self.checkin = checkout_date
