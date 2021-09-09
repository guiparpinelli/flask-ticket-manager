import pytest
import random
from datetime import date

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
    add_event_tickets,
    reduce_event_tickets,
)
from src.tickets.crud import (
    get_ticket_status_by_id,
    get_available_tickets_by_event_id,
    get_redeemed_tickets_by_event_id,
)


def test_get_user_by_id(users):
    user = get_user_by_id(users[0].id)
    assert user.id == users[0].id


def test_get_user_by_email(users):
    user = get_user_by_email(users[0].email)
    assert user.email == users[0].email


def test_create_user_writes_to_db(test_app_context):
    new_user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    db_user = create_user(new_user)
    assert db_user.name == new_user.name
    assert db_user.email == new_user.email
    assert db_user.password != new_user.password


def test_get_events_returns_a_list_of_events(events):
    all_events = get_events()
    assert len(all_events) == len(events)

    two_events = get_events(limit=2)
    assert len(two_events) == 2


def test_create_event_writes_to_db(users):
    new_event = EventCreate(name="Pycon", date="2021-01-09")
    db_event = create_event(new_event, users[0].id)
    assert db_event.name == new_event.name
    assert db_event.date == new_event.date
    assert db_event.admin_id == users[0].id


def test_get_events_by_datetime_period_returns_list_of_events_between_dates(events):
    # Events factory creates events with current year date
    this_year = date.today().year
    start = date(this_year, 1, 1)
    end = date(this_year, 12, 31)
    e = get_events_by_datetime_period(start, end)

    assert e is not None
    assert len(e) == len(events)


def test_get_event_by_id_returns_db_event_obj(events):
    db_event = get_event_by_id(events[0].id)
    assert db_event.id == events[0].id


def test_get_event_by_name_returns_db_event_obj(events):
    db_event = get_event_by_name(events[0].name)
    assert db_event.name == events[0].name


def test_update_max_tickets_successefully_updates_db_event(make_event):
    db_event = make_event(max_tickets=0)
    assert db_event.max_tickets == 0
    new_event = EventUpdate(max_tickets=10)
    obj_in = new_event.dict(exclude_unset=True)
    updated_event = update_max_tickets(db_event, obj_in)
    assert updated_event.max_tickets == 10


def test_get_ticket_status_by_id_returns_redeem_status(events):
    ticket = events[0].tickets[0]
    is_redeemed = get_ticket_status_by_id(ticket.id)
    assert not is_redeemed


def test_add_event_tickets_adds_total_difference_of_tickets_to_events_ticket_list(
    make_event,
):
    db_event = make_event(max_tickets=5)
    assert db_event.max_tickets == 5
    assert len(db_event.tickets) == 5
    db_event.max_tickets = 10
    add_event_tickets(db_event)
    assert db_event.max_tickets == 10
    assert len(db_event.tickets) == 10


def test_reduce_event_tickets_raise_error_when_trying_to_reduce_below_total_of_redeemed_tickets(
    make_event, users
):
    db_event = make_event(max_tickets=5)
    assert db_event.max_tickets == 5
    assert len(db_event.tickets) == 5

    for ticket in db_event.tickets:
        ticket.redeem_ticket(random.choice(users).id)

    db_event.max_tickets = 1

    with pytest.raises(ValueError):
        reduce_event_tickets(db_event)


def test_reduce_event_tickets_reduces_tickets_to_new_max_tickets(make_event, users):
    db_event = make_event(max_tickets=5)
    assert db_event.max_tickets == 5
    assert len(db_event.tickets) == 5

    for ticket in db_event.tickets[:2]:
        ticket.redeem_ticket(random.choice(users).id)

    db_event.max_tickets = 4
    updated_ticket_list = reduce_event_tickets(db_event)

    assert len(updated_ticket_list) == 4
    assert updated_ticket_list[0].is_redeemed
    assert updated_ticket_list[1].is_redeemed
    assert not updated_ticket_list[2].is_redeemed


def test_get_available_tickets_returns_event_not_redeemed_tickets(make_event, users):
    db_event = make_event(max_tickets=5)

    for ticket in db_event.tickets[:2]:
        ticket.redeem_ticket(users[0].id)

    available_tickets = get_available_tickets_by_event_id(db_event.id)
    assert len(available_tickets) == 3


def test_get_redeemed_tickets_returns_event_redeemed_tickets(make_event, users):
    db_event = make_event(max_tickets=5)

    for ticket in db_event.tickets[:2]:
        ticket.redeem_ticket(users[0].id)

    redeemed_tickets = get_redeemed_tickets_by_event_id(db_event.id)
    assert len(redeemed_tickets) == 2
