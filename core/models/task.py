from sqlalchemy.orm import Mapped

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Task(IntIdPkMixin, Base):
    title: Mapped[str]
    pomodoro_count: Mapped[int]
