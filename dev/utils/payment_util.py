class PaymentMethod:
    def pay(self, amount):
        pass


class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        return f"Paid {amount} by credit card"


class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        return f"Paid {amount} by PayPal"
