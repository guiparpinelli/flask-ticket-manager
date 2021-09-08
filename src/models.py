from flask import current_app

from src import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(60))
    events = db.relationship("Event", backref="admin", lazy="dynamic")

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = self._generate_password_hash(password)

    def is_password_correct(self, password_plaintext: str) -> bool:
        return bcrypt.check_password_hash(self.password, password_plaintext)

    def set_password(self, password_plaintext: str) -> None:
        self.password = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext: str) -> str:
        return bcrypt.generate_password_hash(
            password_plaintext, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")

    def __repr__(self):
        return f"<User: {self.email}>"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String, nullable=True)
    max_tickets = db.Column(db.Integer, default=0)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tickets = db.relationship("Ticket", backref="event", lazy="dynamic")

    def __repr__(self):
        return f"<Event: {self.name}>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    redeemed = db.Column(db.Boolean, default=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # TODO add constraints to prevent redeemed to be True if owner_id is None

    def __repr__(self):
        return f"<Ticket: {self.id}>"

    @property
    def is_redeemed(self) -> bool:
        return self.redeemed
