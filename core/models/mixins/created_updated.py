from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column


class CreatedUpdatedMixin:
    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())")
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=func.now(),
    )
