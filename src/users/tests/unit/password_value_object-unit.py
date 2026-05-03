import pytest
from src.users.domain.password import Password


def test_valid_password_is_accepted():
    pwd = Password.create("secret123")
    assert pwd.value == "secret123"


def test_short_password_raises():
    with pytest.raises(ValueError, match="at least 6"):
        Password.create("abc")


def test_minimum_length_is_accepted():
    pwd = Password.create("abcdef")
    assert pwd.value == "abcdef"
