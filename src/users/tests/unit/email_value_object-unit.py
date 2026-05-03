import pytest
from src.shared.domain.email import Email

def test_valid_email_is_normalised():
    email = Email.create("  User@Example.COM  ")
    assert email.value == "user@example.com"


def test_invalid_email_raises():
    with pytest.raises(ValueError):
        Email.create("not-an-email")


def test_missing_domain_raises():
    with pytest.raises(ValueError):
        Email.create("user@")


def test_missing_local_raises():
    with pytest.raises(ValueError):
        Email.create("@example.com")


def test_str_returns_value():
    assert str(Email.create("test@example.com")) == "test@example.com"


def test_equal_emails_are_equal():
    assert Email.create("A@B.com") == Email.create("a@b.com")
