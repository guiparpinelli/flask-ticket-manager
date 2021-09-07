def test_user_password_is_being_hashed(new_user):
    assert new_user.password != "TestUser123"


def test_user_correct_password_can_be_decrypted(new_user):
    assert new_user.is_password_correct("TestUser123")


def test_event_organizer_id_is_equal_to_user_id(new_event, new_user):
    assert new_event.organizer_id == new_user.id


def test_event_max_tickets_defaults_to_zero_if_not_set(new_event):
    assert new_event.max_tickets == 0
