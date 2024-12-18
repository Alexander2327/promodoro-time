from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_updated import CreatedUpdatedMixin

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Task(IntIdPkMixin, CreatedUpdatedMixin, Base):
    title: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categorys.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="tasks")
    category: Mapped["Category"] = relationship(back_populates="tasks")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
