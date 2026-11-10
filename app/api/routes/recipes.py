"""
API routes for Recipe operations.

Provides endpoints to list all recipes and retrieve a single recipe by ID.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.recipe import RecipeRead
from app.services.recipe_service import get_recipe_by_id, get_recipes


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)

# Reusable dependency annotation for database sessions
DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "/",
    response_model=list[RecipeRead],
)
def read_recipes(db: DbSession):
    """
    Retrieve a list of all recipes.

    Returns:
        list[RecipeRead]: A list of recipes serialized via Pydantic.
    """
    recipes = get_recipes(db)

    return recipes


@router.get(
    "/{recipe_id}",
    response_model=RecipeRead,
)
def read_recipe(recipe_id: int, db: DbSession):
    """
    Retrieve a specific recipe by its ID.

    Args:
        recipe_id (int): The unique identifier of the recipe.

    Raises:
        HTTPException: 404 error if the recipe does not exist.

    Returns:
        RecipeRead: The requested recipe data.
    """
    recipe = get_recipe_by_id(db, recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found.",
        )

    return recipe