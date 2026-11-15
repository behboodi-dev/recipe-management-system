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
    """
    recipe = db.get(Recipe, recipe_id)

    return recipe


def get_owned_recipe(
    db: Session,
    recipe_id: int,
    user_id: int,
) -> Recipe | None:
    """
    Retrieve a recipe only if it belongs to the given user.
    """
    statement = select(Recipe).where(
        Recipe.id == recipe_id,
        Recipe.user_id == user_id,
    )

    recipe = db.scalars(statement).one_or_none()

    return recipe


def create_recipe(
    db: Session,
    user_id: int,
    recipe_data: RecipeCreate,
) -> Recipe:
    """
    Create a new recipe.
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


def update_recipe(
    db: Session,
    recipe_id: int,
    user_id: int,
    recipe_data: RecipeUpdate,
) -> Recipe | None:
    """
    Update an existing recipe if it belongs to the given user.

    Args:
        db (Session): The database session.
        recipe_id (int): The ID of the recipe to update.
        user_id (int): The ID of the user requesting the update.
        recipe_data (RecipeUpdate): The validated update data.

    Returns:
        Recipe | None: The updated recipe, or None if not found/unauthorized.

    Raises:
        IntegrityError: If a database constraint is violated.
    """
    recipe = get_owned_recipe(
        db=db,
        recipe_id=recipe_id,
        user_id=user_id,
    )

    if recipe is None:
        return None

    update_data = recipe_data.model_dump()

    for field, value in update_data.items():
        setattr(recipe, field, value)

    try:
        db.commit()
        db.refresh(recipe)

    except IntegrityError:
        db.rollback()
        raise

    return recipe


def delete_recipe(
    db: Session,
    recipe_id: int,
    user_id: int,
) -> bool:
    """
    Delete a recipe if it belongs to the given user.

    Args:
        db (Session): The database session.
        recipe_id (int): The ID of the recipe to delete.
        user_id (int): The ID of the user requesting the deletion.

    Returns:
        bool: True if the recipe was deleted successfully, 
              False if it was not found or does not belong to the user.

    Raises:
        IntegrityError: If a database constraint prevents deletion.
    """
    recipe = get_owned_recipe(
        db=db,
        recipe_id=recipe_id,
        user_id=user_id,
    )

    if recipe is None:
        return False

    try:
        db.delete(recipe)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

    return True