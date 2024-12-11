from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, func, text

from datetime import datetime


class CreatedUpdatedMixin:
    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())")
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"),
        onupdate=func.now()
    )
