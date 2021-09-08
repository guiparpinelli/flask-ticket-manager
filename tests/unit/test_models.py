def test_user_password_is_being_hashed(users):
    assert users[0].password != "test1212"


def test_user_correct_password_can_be_decrypted(users):
    assert users[0].is_password_correct("test1212")


def test_event_generates_tickets_when_max_tickets_is_passed(make_event):
    event = make_event(max_tickets=2)
    assert event.max_tickets == 2
    assert len(event.tickets) == 2
