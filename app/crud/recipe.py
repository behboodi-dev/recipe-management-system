from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Recipe


UPDATABLE_FIELDS = {
    "title",
    "description",
    "prep_time_minutes",
    "cook_time_minutes",
    "servings",
    "image_url",
}


def validate_recipe_data(data):
    """Validate recipe fields (title, times, servings) before saving."""

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            raise ValueError("Recipe title cannot be empty.")

    for field in ("prep_time_minutes", "cook_time_minutes"):
        if field in data:
            value = data[field]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{field} must be a non-negative integer.")

    if "servings" in data:
        value = data["servings"]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("Servings must be a positive integer.")


def create_recipe(
    session: Session,
    user_id: int,
    title: str,
    prep_time_minutes: int,
    cook_time_minutes: int,
    servings: int,
    description: str | None = None,
    image_url: str | None = None,
):
    """Create a new recipe and add it to the database."""

    data = {
        "title": title,
        "prep_time_minutes": prep_time_minutes,
        "cook_time_minutes": cook_time_minutes,
        "servings": servings,
    }

    validate_recipe_data(data)

    recipe = Recipe(
        user_id=user_id,
        title=title.strip(),
        description=description,
        prep_time_minutes=prep_time_minutes,
        cook_time_minutes=cook_time_minutes,
        servings=servings,
        image_url=image_url,
    )

    session.add(recipe)
    session.flush()

    return recipe


def get_recipe(
    session: Session,
    recipe_id: int,
    user_id: int | None = None,
):
    """Get a single recipe by ID, optionally filtered by user ID."""

    statement = select(Recipe).where(Recipe.id == recipe_id)

    if user_id is not None:
        statement = statement.where(Recipe.user_id == user_id)

    return session.scalars(statement).first()


def get_recipes(
    session: Session,
    user_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
):
    """Get a paginated list of recipes, optionally filtered by user ID."""

    if offset < 0:
        raise ValueError("Offset cannot be negative.")

    if limit <= 0:
        raise ValueError("Limit must be positive.")

    statement = select(Recipe)

    if user_id is not None:
        statement = statement.where(Recipe.user_id == user_id)

    statement = (
        statement
        .order_by(Recipe.created_at.desc(), Recipe.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(session.scalars(statement).all())


def update_recipe(
    session: Session,
    recipe_id: int,
    user_id: int,
    **updates,
):
    """Update a recipe's fields, ensuring only allowed fields are changed."""

    if not updates:
        raise ValueError("At least one field must be provided for update.")

    invalid_fields = set(updates) - UPDATABLE_FIELDS

    if invalid_fields:
        raise ValueError(
            f"Fields cannot be updated: {', '.join(sorted(invalid_fields))}"
        )

    validate_recipe_data(updates)

    recipe = get_recipe(
        session=session,
        recipe_id=recipe_id,
        user_id=user_id,
    )

    if recipe is None:
        return None

    for field, value in updates.items():
        if field == "title":
            value = value.strip()

        setattr(recipe, field, value)

    session.flush()

    return recipe


def delete_recipe(
    session: Session,
    recipe_id: int,
    user_id: int,
):
    """Delete a recipe if the specified user is the owner."""

    recipe = get_recipe(
        session=session,
        recipe_id=recipe_id,
        user_id=user_id,
    )

    if recipe is None:
        return False

    session.delete(recipe)
    session.flush()

    return True