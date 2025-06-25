from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
import datetime


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_on: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_on: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
