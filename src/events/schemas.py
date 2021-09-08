from datetime import datetime
from src.users.schemas import User
from typing import Optional, List
from dateutil import parser
from pydantic import BaseModel, validator

from src.users.schemas import User
from src.tickets.schemas import Ticket


class EventBase(BaseModel):
    name: str
    date: datetime
    description: Optional[str] = None
    max_tickets: int = 0

    @validator("date", pre=True)
    def parse_date(cls, date: str) -> datetime:
        return parser.parse(date)


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    admin_id: int
    tickets: Optional[List[Ticket]] = []

    class Config:
        orm_mode = True


class EventUpdate(EventBase):
    name: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    max_tickets: Optional[int] = None
