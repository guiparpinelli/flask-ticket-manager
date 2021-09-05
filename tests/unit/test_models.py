from datetime import datetime


def test_user_password_is_being_hashed(new_user):
    assert new_user.password != "TestUser123"


def test_user_correct_password_can_be_decrypted(new_user):
    assert new_user.is_password_correct("TestUser123")


def test_event_date_parser_is_returning_datetime_object(new_event):
    assert isinstance(new_event.date, datetime)
