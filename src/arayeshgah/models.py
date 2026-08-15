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


class WorkHour(Base):
    """
    One working range per weekday.

    Example:
    barber_id=1
    weekday=0
    start_minute=480   -> 08:00
    end_minute=720     -> 12:00
    """

    __tablename__ = "work_hours"

    __table_args__ = UniqueConstraint(
        "barber_id",
        "weekday",
        name="uq_work_hours_barber_weekday",
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    barber_id: Mapped[int] = mapped_column(
        ForeignKey("barbers.id", ondelete="CASCADE"), index=True
    )
    weekday: Mapped[int] = mapped_column(Integer)
    start_minute: Mapped[int] = mapped_column(Integer)
    end_minute: Mapped[int] = mapped_column(Integer)


class Appointment(Base):
    __tablename__ = "appointments"

    __table_args__ = Index(
        "ix_appointments_barber_time",
        "barber_id",
        "start_at",
        "end_at",
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    barber_id: Mapped[int] = mapped_column(
        ForeignKey("barbers.id", ondelete="CASCADE"), index=True
    )
    customer_telegram_id: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )  # Some users might dont have username yet
    customer_first_name: Mapped[str] = mapped_column(String(100))

    customer_last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(30))
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)

    status: Mapped[AppointmentStatus] = mapped_column(
        SAEnum(AppointmentStatus, native_enum=False, length=20),
        default=AppointmentStatus.PENDING,
    )
    pending_expires_in: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now_naive,
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        onupdate=utc_now_naive,
        nullable=True,
    )
