from src import db, models
from src.users import schemas


def get_user(user_id: int) -> models.User:
    return db.session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(user_email: str) -> models.User:
    return db.session.query(models.User).filter(models.User.email == user_email).first()


def create_user(user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db.session.add(db_user)
    db.session.commit()
    return db_user
