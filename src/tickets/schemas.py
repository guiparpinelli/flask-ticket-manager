from typing import Optional
from pydantic import BaseModel


class TicketBase(BaseModel):
    event_id: int


class TicketUpdate(TicketBase):
    redeemed: bool


class Ticket(TicketBase):
    id: int
    redeemed: bool = False
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True
