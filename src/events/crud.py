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


def update_max_tickets(db_event: models.Event, max_tickets: int) -> models.Event:
    pass
