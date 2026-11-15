# """
# Service layer for Recipe operations.

# Handles business logic for retrieving, creating, and managing recipes
# in the database.
# """

# from sqlalchemy import select
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session

# from app.models import Recipe
# from app.schemas.recipe import RecipeCreate, RecipeUpdate


# def get_recipes(db: Session) -> list[Recipe]:
#     """
#     Retrieve a list of all recipes, ordered by their ID.

#     Args:
#         db (Session): The database session.

#     Returns:
#         list[Recipe]: A list of all recipe objects in the database.
#     """
#     statement = select(Recipe).order_by(Recipe.id)

#     recipes = db.scalars(statement).all()

#     return recipes


# def get_recipe_by_id(
#     db: Session,
#     recipe_id: int,
# ) -> Recipe | None:
#     """
#     Retrieve a specific recipe by its ID.

#     Args:
#         db (Session): The database session.
#         recipe_id (int): The unique identifier of the recipe.

#     Returns:
#         Recipe | None: The recipe object if found, otherwise None.
#     """
#     statement = select(Recipe).where(
#         Recipe.id == recipe_id
#     )

#     recipe = db.scalars(statement).first()
    

#     return recipe


# def create_recipe(
#     db: Session,
#     user_id: int,
#     recipe_data: RecipeCreate,
# ) -> Recipe:
#     """
#     Create a new recipe in the database.

#     Args:
#         db (Session): The database session.
#         user_id (int): The ID of the user who owns the recipe.
#         recipe_data (RecipeCreate): The validated recipe data from Pydantic.

#     Returns:
#         Recipe: The newly created and refreshed Recipe object.

#     Raises:
#         IntegrityError: If a database constraint is violated 
#                         (e.g., foreign key error).
#     """
#     recipe = Recipe(
#         user_id=user_id,
#         **recipe_data.model_dump(),
#     )

#     try:
#         db.add(recipe)
#         db.commit()
#         db.refresh(recipe)

#     except IntegrityError:
#         db.rollback()
#         raise

#     return recipe


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
