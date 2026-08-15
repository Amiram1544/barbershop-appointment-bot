from datetime import datetime, timezone
from enum import IntEnum, Enum as PyEnum
from typing import Optional
from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Base(DeclarativeBase):
    """
    Base class used for declarative class definitions.
    """

    pass


class Weekday(IntEnum):
    SATURDAY = 0
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6


class ConfirmationMode(str, PyEnum):
    AUTO = "auto"
    MANUAL = "manual"


class AppointmentStatus(str, PyEnum):
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    PENDING = "pending"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Barber(Base):
    __tablename__ = "barbers"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_user_id: Mapped[int] = mapped_column(
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    location_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    confirmation_mode: Mapped[ConfirmationMode] = mapped_column(
        SAEnum(ConfirmationMode, native_enum=False, length=20),
        default=ConfirmationMode.MANUAL,
    )
    service_duration_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    slot_step_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now_naive,
    )
