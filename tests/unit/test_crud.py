from src.users.schemas import UserCreate
from src.events.schemas import EventCreate
from src.users.crud import get_user_by_id, get_user_by_email, create_user
from src.events.crud import create_event


def test_get_user_by_id(test_app_context, new_user):
    user = get_user_by_id(new_user.id)
    assert user.id == new_user.id


def test_get_user_by_email(test_app_context, new_user):
    user = get_user_by_email(new_user.email)
    assert user.email == new_user.email


def test_create_user_writes_to_db(test_app_context):
    new_user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    db_user = create_user(new_user)
    assert db_user.name == new_user.name
    assert db_user.email == new_user.email
    assert db_user.password != new_user.password


# TODO create a event factory
def test_get_events_returns_a_list_of_events(test_app_context):
    pass


def test_create_event_writes_to_db(test_app_context, new_user):
    new_event = EventCreate(name="Pycon", date="2021-01-09")
    db_event = create_event(new_event, new_user.id)
    assert db_event.name == new_event.name
    assert db_event.date == new_event.date
    assert db_event.admin_id == new_user.id
