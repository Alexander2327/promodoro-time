from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.created_updated import CreatedUpdatedMixin
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user import User


class Profile(IntIdPkMixin, CreatedUpdatedMixin, Base):
    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["User"] = relationship(back_populates="profile")
