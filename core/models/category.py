from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_updated import CreatedUpdatedMixin


if TYPE_CHECKING:
    from .task import Task


class Category(IntIdPkMixin, CreatedUpdatedMixin, Base):
    name: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="category")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
