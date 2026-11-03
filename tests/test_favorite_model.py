"""
Tests for the Favorite model.

Verifies that favorite records can be read
and their relationships are valid.
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models.user import User
from app.models.recipe import Recipe
from app.models.favorite import Favorite


def test_read_favorites():
    """Test reading favorites from the database."""

    with SessionLocal() as session:
        statement = select(Favorite).limit(5)
        favorites = session.scalars(statement).all()

        assert isinstance(favorites, list)

        for favorite in favorites:
            assert isinstance(favorite, Favorite)
            assert favorite.user_id is not None
            assert favorite.recipe_id is not None

        print("Successfully queried the favorites table.")
        print(f"Found {len(favorites)} favorite(s).")


def test_favorite_user_exists():
    """Test that each favorite record references an existing user."""

    with SessionLocal() as session:
        statement = select(Favorite).limit(5)
        favorites = session.scalars(statement).all()

        for favorite in favorites:
            user = session.get(User, favorite.user_id)
            assert user is not None


def test_favorite_recipe_exists():
    """Test that each favorite record references an existing recipe."""

    with SessionLocal() as session:
        statement = select(Favorite).limit(5)
        favorites = session.scalars(statement).all()

        for favorite in favorites:
            recipe = session.get(Recipe, favorite.recipe_id)
            assert recipe is not None

if __name__ == "__main__":
    test_read_favorites()
    test_favorite_user_exists()
    test_favorite_recipe_exists()