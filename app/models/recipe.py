"""
Recipe model for the Recipe Management System.

Maps the `recipes` table, storing core recipe information (title,
description, times, servings) and linking each recipe to its owner
(User) and other related entities.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Recipe(Base):
    """
    Represents a cooking recipe.

    Each recipe belongs to one user and can have many steps, ingredients,
    categories, and favorites.
    """

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    prep_time_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    cook_time_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    servings: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    image_url: Mapped[str | None] = mapped_column(
        Text,
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

    # --- Temporarily commented out until related models are implemented ---
    
    # # Many-to-One (Recipe belongs to one User)
    # user: Mapped["User"] = relationship(
    #     "User",
    #     back_populates="recipes",
    # )

    # # One-to-Many (Recipe has many steps)
    # steps: Mapped[list["RecipeStep"]] = relationship(
    #     "RecipeStep",
    #     back_populates="recipe",
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    #     order_by="RecipeStep.step_number",
    # )

    # # One-to-Many (Recipe has many ingredients)
    # ingredients: Mapped[list["RecipeIngredient"]] = relationship(
    #     "RecipeIngredient",
    #     back_populates="recipe",
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    # )

    # # One-to-Many (Recipe belongs to many categories)
    # categories: Mapped[list["RecipeCategory"]] = relationship(
    #     "RecipeCategory",
    #     back_populates="recipe",
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    # )

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite",
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )