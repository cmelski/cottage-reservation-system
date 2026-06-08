from dev.utils.payment_util import CreditCardPayment, PayPalPayment


def test_payment_by_cc():

    cc_payment = CreditCardPayment()
    result = cc_payment.pay(1000.00)
    print(f'{result}')
    assert 'credit card' in result

def test_payment_by_paypal():

    pp_payment = PayPalPayment()
    result = pp_payment.pay(2000.55)
    print(f'{result}')
    assert 'PayPal' in result

