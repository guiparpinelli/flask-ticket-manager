from pydantic import BaseModel


class TicketBase(BaseModel):
    event_id: int


class Ticket(TicketBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
