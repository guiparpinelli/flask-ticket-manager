from .schemas import UserBase, UserCreate, User
from .crud import create_user
from .forms import RegistrationForm

from flask import Blueprint

users_blueprint = Blueprint("users", __name__, template_folder="templates")

from . import routes
