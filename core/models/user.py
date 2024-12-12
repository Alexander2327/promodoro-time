from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.created_updated import CreatedUpdatedMixin
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .task import Task
    from .profile import Profile


class User(IntIdPkMixin, CreatedUpdatedMixin, Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)