from typing import Optional
from pydantic import BaseModel


class TicketBase(BaseModel):
    redeemed: bool = False


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    event_id: int
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True
