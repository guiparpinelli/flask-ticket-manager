from typing import List
from src import db, models
from src.events import schemas


def get_events(skip: int = 0, limit: int = 100) -> List[models.Event]:
    return db.session.query(models.Event).offset(skip).limit(limit).all()


def create_event(event: schemas.EventCreate) -> models.Event:
    db_event = models.User(**event.dict())
    db.session.add(db_event)
    db.session.commit()
    return db_event
