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
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")