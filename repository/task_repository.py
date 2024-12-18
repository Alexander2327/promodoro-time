from core.models import Task
from repository.base_repository import Repository


class TaskRepository(Repository):
    model = Task
