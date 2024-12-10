from sqlalchemy.orm import Mapped

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_updated import CreatedUpdatedMixin


class Category(IntIdPkMixin, CreatedUpdatedMixin, Base):
    name: Mapped[str]