def test_user_password_is_being_hashed(users):
    assert users[0].password != "test1212"


def test_user_correct_password_can_be_decrypted(users):
    assert users[0].is_password_correct("test1212")


def test_event_max_tickets_defaults_to_zero_if_not_set(events):
    assert events[0].max_tickets == 0
