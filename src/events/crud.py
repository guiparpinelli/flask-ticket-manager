from typing import List
from datetime import datetime
from sqlalchemy import and_

from src import db, models
from src.events import schemas


def get_events(skip: int = 0, limit: int = 100) -> List[models.Event]:
    return db.session.query(models.Event).offset(skip).limit(limit).all()


def get_event_by_name(name: str) -> models.Event:
    return db.session.query(models.Event).filter(models.Event.name == name).first()


def get_event_by_id(id: int) -> models.Event:
    return db.session.query(models.Event).filter(models.Event.id == id).first()


def get_events_by_datetime_period(
    start_date: datetime, end_date: datetime
) -> List[models.Event]:
    return (
        db.session.query(models.Event)
        .filter(and_(models.Event.date >= start_date, models.Event.date <= end_date))
        .all()
    )


def create_event(event: schemas.EventCreate, user_id: int) -> models.Event:
    db_event = models.Event(**event.dict(), admin_id=user_id)
    db.session.add(db_event)
    db.session.commit()
    return db_event


def add_event_tickets(db_event: models.Event) -> models.Event:
    current_tickets = list(db_event.tickets)
    difference = db_event.max_tickets - len(current_tickets)
    new_tickets_list = current_tickets + [
        models.Ticket(event_id=db_event.id) for _ in range(difference)
    ]
    db_event.tickets = new_tickets_list
    db.session.commit()
    db.session.refresh(db_event)
    return db_event


def reduce_event_tickets(db_event: models.Event) -> models.Event:
    redeemed_tickets = list(filter(lambda x: x.is_redeemed, db_event.tickets))
    if db_event.max_tickets < len(redeemed_tickets):
        raise ValueError(
            f"Cannot reduce max tickets below total of currently redeemed tickets: {len(redeemed_tickets)}"
        )
    new_tickets_list = redeemed_tickets + [not t.is_redeemed for t in db_event.tickets]
    db_event.tickets = new_tickets_list
    db.session.commit()
    db.session.refresh(db_event)
    return db_event


def update_max_tickets(
    db_event: models.Event, obj_in: schemas.EventUpdate
) -> models.Event:
    for key, value in obj_in.items():
        setattr(db_event, key, value)
    db.session.add(db_event)
    db.session.commit()
    db.session.refresh(db_event)
    return db_event
