from dev.utils.generic_utils import valid_email


def test_valid_email():
    assert valid_email("test@example.com") is True
    assert valid_email("john.doe+qa@gmail.com") is True


def test_invalid_email():
    assert valid_email("bad-email") is False
    assert valid_email("@gmail.com") is False
