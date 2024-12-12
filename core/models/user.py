from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.created_updated import CreatedUpdatedMixin
from core.models.mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, CreatedUpdatedMixin, Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)