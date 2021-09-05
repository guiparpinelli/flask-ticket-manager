from typing import Optional
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None


class EventCreate(EventBase):
    max_tickets: int = 0


class Event(EventBase):
    id: int
    organizer_id: int

    class Config:
        orm_mode = True
