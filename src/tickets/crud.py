from typing import List, Tuple

from src import db, models
from src.tickets import schemas


def get_ticket_status_by_id(ticket_id: int) -> bool:
    return (
        db.session.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
        .is_redeemed
    )
