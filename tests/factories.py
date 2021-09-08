import random
import factory
from faker import Faker

from src import models, db


fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ("email",)
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("name")
    email = factory.Faker("email")
    password = "test1212"


class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Event
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ("name",)
        sqlalchemy_session_persistence = "flush"

    name = factory.Iterator(("Pycon", "DjangoCon", "SciPy"))
    date = factory.Faker("date_this_year", after_today=True)
    description = "An awesome Python conference"
    max_tickets = 10
    admin_id = factory.LazyAttribute(lambda n: UserFactory().id)


class TicketFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Ticket
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ("id",)
        sqlalchemy_session_persistence = "flush"

    id = factory.Sequence(lambda n: n)
    redeemed = random.choice((True, False))
    event_id = factory.LazyAttribute(lambda n: EventFactory().id)
    owner_id = factory.LazyAttribute(lambda n: UserFactory().id if redeemed else None)
