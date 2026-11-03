
"""
Tests for the Recipe model.

Verifies that the Recipe model can communicate
with the PostgreSQL database.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.recipe import Recipe


def test_read_recipes():
    """Test reading recipes from the database."""

    with SessionLocal() as session:

        statement = select(Recipe).limit(5)

        recipes = session.scalars(statement).all()

        assert isinstance(recipes, list)

        for recipe in recipes:
            assert isinstance(recipe, Recipe)
            assert recipe.id is not None
            assert recipe.title is not None

        print(f"Successfully queried the recipes table.")
        print(f"Found {len(recipes)} recipe(s).")

if __name__ == "__main__":
    test_read_recipes()