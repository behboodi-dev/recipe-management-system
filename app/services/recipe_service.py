"""
Service layer for Recipe operations.

Handles business logic for retrieving recipes from the database.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Recipe


def get_recipes(db: Session) -> list[Recipe]:
    """
    Retrieve a list of all recipes, ordered by their ID.

    Args:
        db (Session): The database session.

    Returns:
        list[Recipe]: A list of all recipe objects in the database.
    """
    statement = select(Recipe).order_by(Recipe.id)

    recipes = db.scalars(statement).all()

    return recipes


def get_recipe_by_id(
    db: Session,
    recipe_id: int,
) -> Recipe | None:
    """
    Retrieve a specific recipe by its ID.

    Args:
        db (Session): The database session.
        recipe_id (int): The unique identifier of the recipe.

    Returns:
        Recipe | None: The recipe object if found, otherwise None.
    """
    statement = select(Recipe).where(
        Recipe.id == recipe_id
    )

    recipe = db.scalars(statement).first()

    return recipe