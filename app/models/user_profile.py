"""
UserProfile model.

Maps the `user_profiles` table (optional profile info) linked one-to-one with users.
"""

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class UserProfile(Base):
    """Represents a user's optional profile information."""

    __tablename__ = "user_profiles"

    __table_args__ = (
        CheckConstraint(
            "username IS NULL OR BTRIM(username) <> ''",
            name="chk_username_not_blank",
        ),
        CheckConstraint(
            "email IS NULL OR BTRIM(email) <> ''",
            name="chk_email_not_blank",
        ),
        Index(
            "uq_user_profiles_username_lower",
            text("LOWER(BTRIM(username))"),
            unique=True,
            postgresql_where=text("username IS NOT NULL"),
        ),
        Index(
            "uq_user_profiles_email_lower",
            text("LOWER(BTRIM(email))"),
            unique=True,
            postgresql_where=text("email IS NOT NULL"),
        ),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    username: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # One-to-One relationship back to User
    user: Mapped["User"] = relationship("User", back_populates="profile")