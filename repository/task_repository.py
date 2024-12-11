from repository.base_repository import Repository
from core.models import Task


class TaskRepository(Repository):
    model = Task