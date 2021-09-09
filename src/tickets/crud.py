from typing import List

from src import db, models


def get_ticket_status_by_id(ticket_id: int) -> bool:
    return (
        db.session.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
        .is_redeemed
    )


def get_redeemed_tickets_by_event_id(event_id: int) -> List[models.Ticket]:
    return (
        db.session.query(models.Ticket)
        .filter(models.Ticket.event_id == event_id)
        .filter(models.Ticket.redeemed)
        .all()
    )


def get_available_tickets_by_event_id(event_id: int) -> List[models.Ticket]:
    return (
        db.session.query(models.Ticket)
        .filter(models.Ticket.event_id == event_id)
        .filter(models.Ticket.redeemed == False)
        .all()
    )
