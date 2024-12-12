from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_updated import CreatedUpdatedMixin


class Task(IntIdPkMixin, CreatedUpdatedMixin, Base):
    title: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id", ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
