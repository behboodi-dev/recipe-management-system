"""
Favorite model for the Recipe Management System.

Maps the `favorites` table, resolving the many-to-many relationship
between users and their favorite recipes.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Favorite(Base):
    """
    Represents a recipe saved as a favorite by a user.

    A user can favorite many recipes, and a recipe can be favorited by many users.
    """

    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    recipe_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="favorites",
    )

    recipe: Mapped["Recipe"] = relationship(
        "Recipe",
        back_populates="favorites",
    )