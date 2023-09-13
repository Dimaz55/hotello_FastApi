from app.repository.base import BaseRepo
from app.users.models import User


class UserRepo(BaseRepo):
    model = User
