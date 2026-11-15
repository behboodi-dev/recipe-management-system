"""
API routes for Recipe operations.

Provides endpoints to create, read, update, and delete recipes.
"""

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import (
    CurrentUser,
    DbSession,
)
from app.schemas.recipe import (
    RecipeCreate,
    RecipeRead,
    RecipeUpdate,
)
from app.services.recipe_service import (
    create_recipe,
    delete_recipe,
    get_recipe_by_id,
    get_recipes,
    update_recipe,
)

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
)


@router.get(
    "/",
    response_model=list[RecipeRead],
)
def read_recipes(db: DbSession):
    """Retrieve all recipes."""
    recipes = get_recipes(db)
    return recipes


@router.get(
    "/{recipe_id}",
    response_model=RecipeRead,
)
def read_recipe(
    recipe_id: int,
    db: DbSession,
):
    """Retrieve a specific recipe by its ID."""
    recipe = get_recipe_by_id(db, recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found.",
        )

    return recipe


@router.post(
    "/",
    response_model=RecipeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_new_recipe(
    recipe_data: RecipeCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Create a new recipe for the current user."""
    try:
        recipe = create_recipe(
            db=db,
            user_id=current_user.id,
            recipe_data=recipe_data,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create recipe due to a database constraint.",
        )

    return recipe


@router.put(
    "/{recipe_id}",
    response_model=RecipeRead,
)
def update_existing_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update an existing recipe (owner only)."""
    try:
        recipe = update_recipe(
            db=db,
            recipe_id=recipe_id,
            user_id=current_user.id,
            recipe_data=recipe_data,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not update recipe due to a database constraint.",
        )

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found.",
        )

    return recipe


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_recipe(
    recipe_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """Delete a recipe (owner only)."""
    try:
        deleted = delete_recipe(
            db=db,
            recipe_id=recipe_id,
            user_id=current_user.id,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Recipe cannot be deleted because related records "
                "prevent deletion."
            ),
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found.",
        )

    # return None