"""
User model for the Recipe Management System.

Maps the `users` table, handling core account data, OTP verification,
soft-deletion, and timestamps.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Identity,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """
    Represents a user account.

    Accounts are soft-deleted (via `deleted_at`) to preserve recipe ownership.
    """

    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "(phone_number IS NULL) = (phone_verified_at IS NULL)",
            name="chk_users_phone_verification",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    phone_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self):
        """Return a developer-friendly representation of the user."""
        return f"User(id={self.id}, phone_number={self.phone_number})"






    