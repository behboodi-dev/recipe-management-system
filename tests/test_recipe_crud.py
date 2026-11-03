from sqlalchemy.orm import Session

from app.database import engine
from app.models import User, Recipe

from app.crud.recipe import (
    create_recipe,
    get_recipe,
    get_recipes,
    update_recipe,
    delete_recipe,
)


def test_recipe_crud():
    """
    Test the complete CRUD lifecycle for Recipe.

    Covers creation, reading, updating, ownership protection,
    deletion, and input validation.
    """

    with Session(engine) as session:
        try:
            user = User()

            session.add(user)
            session.flush()

            print("User created:", user.id)

            recipe = create_recipe(
                session=session,
                user_id=user.id,
                title="Test Pasta",
                description="A simple pasta recipe",
                prep_time_minutes=10,
                cook_time_minutes=20,
                servings=2,
            )

            print("Recipe created:", recipe.id)

            assert recipe.id is not None
            assert recipe.title == "Test Pasta"
            assert recipe.user_id == user.id

            found_recipe = get_recipe(
                session=session,
                recipe_id=recipe.id,
                user_id=user.id,
            )

            assert found_recipe is not None
            assert found_recipe.title == "Test Pasta"

            print("Read recipe: OK")

            recipes = get_recipes(
                session=session,
                user_id=user.id,
            )

            assert len(recipes) == 1
            assert recipes[0].id == recipe.id

            print("Read recipes: OK")

            updated_recipe = update_recipe(
                session=session,
                recipe_id=recipe.id,
                user_id=user.id,
                title="Updated Pasta",
                servings=4,
            )

            assert updated_recipe is not None
            assert updated_recipe.title == "Updated Pasta"
            assert updated_recipe.servings == 4

            print("Update recipe: OK")

            wrong_owner_result = update_recipe(
                session=session,
                recipe_id=recipe.id,
                user_id=user.id + 999,
                title="Unauthorized Update",
            )

            assert wrong_owner_result is None
            assert recipe.title == "Updated Pasta"

            print("Ownership protection: OK")

            deleted = delete_recipe(
                session=session,
                recipe_id=recipe.id,
                user_id=user.id,
            )

            assert deleted is True

            deleted_recipe = get_recipe(
                session=session,
                recipe_id=recipe.id,
            )

            assert deleted_recipe is None

            print("Delete recipe: OK")

            # 9. Check invalid input
            try:
                create_recipe(
                    session=session,
                    user_id=user.id,
                    title="   ",
                    prep_time_minutes=10,
                    cook_time_minutes=20,
                    servings=2,
                )
                assert False, "Empty title should not be accepted."

            except ValueError:
                print("Input validation: OK")

            print("\nAll Recipe CRUD tests passed!")

        finally:
            session.rollback()
            print("Test transaction rolled back.")


if __name__ == "__main__":
    test_recipe_crud()