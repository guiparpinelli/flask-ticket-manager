import pytest

from src import create_app, db
from src.events.schemas import EventCreate
from src.users.schemas import UserCreate
from src.models import User, Event
from tests import factories


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
def users(test_app_context):
    return factories.UserFactory.create_batch(size=5)


@pytest.fixture
def events(test_app_context):
    return factories.EventFactory.create_batch(size=3)


@pytest.fixture
def make_event(test_app_context):
    def _make_event(**kwargs):
        return factories.EventFactory.create(**kwargs)

    yield _make_event


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
