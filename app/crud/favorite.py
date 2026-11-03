from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Favorite, User, Recipe


def add_favorite(
    session: Session,
    user_id: int,
    recipe_id: int,
):
    """
    Add a recipe to a user's favorites.

    Validates that the user and recipe exist, and prevents duplicates.
    """

    user = session.scalars(
        select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
    ).first()

    if user is None:
        raise ValueError("User does not exist or is deleted.")

    recipe = session.scalars(
        select(Recipe).where(Recipe.id == recipe_id)
    ).first()

    if recipe is None:
        raise ValueError("Recipe does not exist.")

    existing = session.get(
        Favorite,
        (user_id, recipe_id),
    )

    if existing is not None:
        raise ValueError("Recipe is already in favorites.")

    favorite = Favorite(
        user_id=user_id,
        recipe_id=recipe_id,
    )

    session.add(favorite)
    session.flush()

    return favorite


def get_favorite(
    session: Session,
    user_id: int,
    recipe_id: int,
):
    """Get a single favorite relationship by user and recipe IDs."""

    return session.get(
        Favorite,
        (user_id, recipe_id),
    )


def get_user_favorites(
    session: Session,
    user_id: int,
):
    """Get all favorite recipes of a specific user."""

    statement = (
        select(Favorite)
        .join(Recipe, Favorite.recipe_id == Recipe.id)
        .where(
            Favorite.user_id == user_id,
            Recipe.user_id != user_id,
        )
        .order_by(Favorite.created_at.desc())
    )

    return list(session.scalars(statement).all())


def get_recipe_favorites(
    session: Session,
    recipe_id: int,
):
    """Get all favorites records associated with a specific recipe."""

    statement = (
        select(Favorite)
        .where(Favorite.recipe_id == recipe_id)
        .order_by(Favorite.created_at.desc())
    )

    return list(session.scalars(statement).all())


def remove_favorite(
    session: Session,
    user_id: int,
    recipe_id: int,
):
    """Remove a recipe from a user's favorites."""

    favorite = get_favorite(
        session,
        user_id,
        recipe_id,
    )

    if favorite is None:
        return False

    session.delete(favorite)
    session.flush()

    return True