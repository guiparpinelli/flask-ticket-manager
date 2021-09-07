import pytest

from src import create_app, db
from src.events.schemas import EventCreate
from src.users.schemas import UserCreate
from src.models import User, Event


@pytest.fixture(scope="module")
def test_app_context():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    with flask_app.app_context():
        yield


@pytest.fixture(scope="module")
def test_app():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    yield flask_app


@pytest.fixture(scope="module")
def new_user(test_app):
    new_user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    with test_app.app_context():
        user = User(**new_user.dict())
        yield user


@pytest.fixture(scope="module")
def new_event(test_app, new_user):
    new_event = EventCreate(name="Pycon", date="2021-01-09")
    with test_app.app_context():
        event = Event(**new_event.dict(), organizer_id=new_user.id)
        yield event


@pytest.fixture(scope="module")
def test_client(test_app):
    with test_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with test_app.app_context():
            test_app.logger.info("Creating database tables in test_client fixture...")

            # Create the database and the database table(s)
            db.create_all()

        yield testing_client

        with test_app.app_context():
            db.drop_all()


@pytest.fixture(scope="module")
def register_user(test_client):
    user = UserCreate(name="Guilherme", email="hire@me.com", password="TestUser123")
    test_client.post("/register", data={**user.dict()}, follow_redirects=True)
    return


@pytest.fixture(scope="function")
def log_in_user(test_client, register_user):
    test_client.post(
        "/login",
        data={"email": "hire@me.com", "password": "TestUser123"},
        follow_redirects=True,
    )
    yield

    test_client.get("/logout")
