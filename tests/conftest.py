from flask_wtf.recaptcha import widgets
import pytest

from src import create_app, db
from src.events.schemas import EventCreate
from src.users.schemas import UserCreate
from src.models import User, Event


@pytest.fixture
def test_app_context():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    with flask_app.app_context():
        db.create_all()
        yield

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture
def test_client():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()

        yield testing_client

        with flask_app.app_context():
            db.drop_all()


@pytest.fixture
def new_user():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    new_user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    with flask_app.app_context():
        db.create_all()
        user = User(**new_user.dict())
        db.session.add(user)
        db.session.commit()
        yield user

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture
def new_event(new_user):
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    new_event = EventCreate(name="Pycon", date="2021-01-09")
    with flask_app.app_context():
        db.create_all()
        event = Event(**new_event.dict(), admin_id=new_user.id)
        db.session.add(event)
        db.session.commit()
        yield event

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture
def register_user(test_client):
    user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    test_client.post("/register", data={**user.dict()}, follow_redirects=True)
    return


@pytest.fixture
def log_in_user(test_client, register_user):
    test_client.post(
        "/login",
        data={"email": "hire@me.com", "password": "TestUser123"},
        follow_redirects=True,
    )
    yield

    test_client.get("/logout")
