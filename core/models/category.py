from sqlalchemy.orm import Mapped

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Category(IntIdPkMixin, Base):
    name: Mapped[str]