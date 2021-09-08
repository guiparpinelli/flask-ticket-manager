from datetime import date, timedelta

from src.users.schemas import UserCreate
from src.events.schemas import EventCreate, EventUpdate
from src.users.crud import create_user, get_user_by_id, get_user_by_email
from src.events.crud import (
    create_event,
    get_events,
    get_events_by_datetime_period,
    get_event_by_id,
    get_event_by_name,
    update_max_tickets,
)


def test_get_user_by_id(test_app_context, users):
    user = get_user_by_id(users[0].id)
    assert user.id == users[0].id


def test_get_user_by_email(test_app_context, users):
    user = get_user_by_email(users[0].email)
    assert user.email == users[0].email


def test_create_user_writes_to_db(test_app_context):
    new_user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    db_user = create_user(new_user)
    assert db_user.name == new_user.name
    assert db_user.email == new_user.email
    assert db_user.password != new_user.password


def test_get_events_returns_a_list_of_events(test_app_context, events):
    all_events = get_events()
    assert len(all_events) == len(events)

    two_events = get_events(limit=2)
    assert len(two_events) == 2


def test_create_event_writes_to_db(test_app_context, users):
    new_event = EventCreate(name="Pycon", date="2021-01-09")
    db_event = create_event(new_event, users[0].id)
    assert db_event.name == new_event.name
    assert db_event.date == new_event.date
    assert db_event.admin_id == users[0].id


def test_get_events_by_datetime_period_returns_list_of_events_between_dates(
    test_app_context, events
):
    # Events factory creates events with current year date
    this_year = date.today().year
    start = date(this_year, 1, 1)
    end = date(this_year, 12, 31)
    e = get_events_by_datetime_period(start, end)

    assert e is not None
    assert len(e) == len(events)


def test_get_event_by_id_returns_db_event_obj(test_app_context, events):
    db_event = get_event_by_id(events[0].id)
    assert db_event.id == events[0].id


# FIXME
def test_update_max_tickets_successefully_updates_db_event(test_app_context, events):
    new_event = EventUpdate(max_tickets=events[0].max_tickets + 10)
    obj_in = new_event.dict(exclude_unset=True)
    updated_event = update_max_tickets(events[0], obj_in)
    import pdb

    pdb.set_trace()
    assert updated_event.max_tickets != events[0].max_tickets
    assert updated_event.max_tickets == obj_in.get("max_tickets")
    assert updated_event.max_tickets == events[0].max_tickets + 10
