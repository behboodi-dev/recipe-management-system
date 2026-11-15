
"""
Service layer for Recipe operations.

Handles business logic for retrieving, creating, and managing recipes
in the database.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


def get_recipes(db: Session) -> list[Recipe]:
    """
    Retrieve all recipes from the database, ordered by their ID.

    Args:
        db (Session): The database session.

    Returns:
        list[Recipe]: A list of all recipe objects.
    """
    statement = select(Recipe).order_by(Recipe.id)

    recipes = list(db.scalars(statement).all())

    return recipes


def get_recipe_by_id(
    db: Session,
    recipe_id: int,
) -> Recipe | None:
    """
    Retrieve a recipe by its primary key.

    Args:
        db: The database session.
        recipe_id: The recipe's primary key.

    Returns:
        Recipe | None: The recipe if found, otherwise None.
    """
    recipe = db.get(Recipe, recipe_id)

    return recipe


def create_recipe(
    db: Session,
    user_id: int,
    recipe_data: RecipeCreate,
) -> Recipe:
    """
    Create a new recipe.

    Args:
        db: The database session.
        user_id: The ID of the recipe owner.
        recipe_data: Validated recipe data.

    Returns:
        Recipe: The newly created recipe.

    Raises:
        IntegrityError: If a database constraint is violated.
    """
    recipe = Recipe(
        user_id=user_id,
        **recipe_data.model_dump(),
    )

    try:
        db.add(recipe)
        db.commit()
        db.refresh(recipe)

    except IntegrityError:
        db.rollback()
        raise

    return recipe
