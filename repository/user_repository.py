from core.models import User
from repository.base_repository import Repository


class UserRepository(Repository):
    model = User