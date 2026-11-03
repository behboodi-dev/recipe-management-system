from sqlalchemy.orm import Session

from app.database import engine
from app.models import User, Recipe, Favorite

from app.crud.favorite import (
    add_favorite,
    get_favorite,
    get_user_favorites,
    get_recipe_favorites,
    remove_favorite,
)


def test_favorite_crud():
    """
    Test the complete CRUD lifecycle for Favorite.

    Covers adding favorites, preventing duplicates, reading favorites
    by user or recipe, and removing favorites.
    """

    with Session(engine) as session:
        try:
            user = User()
            author = User()

            session.add_all([user, author])
            session.flush()

            recipe = Recipe(
                user_id=author.id,
                title="Favorite Test Recipe",
                prep_time_minutes=10,
                cook_time_minutes=20,
                servings=2,
            )

            session.add(recipe)
            session.flush()

            print("Test data created: OK")

            favorite = add_favorite(
                session,
                user.id,
                recipe.id,
            )

            assert favorite.user_id == user.id
            assert favorite.recipe_id == recipe.id

            print("CREATE Favorite: OK")

            found = get_favorite(
                session,
                user.id,
                recipe.id,
            )

            assert found is not None

            print("READ Favorite: OK")

            user_favorites = get_user_favorites(
                session,
                user.id,
            )

            assert len(user_favorites) == 1
            assert user_favorites[0].recipe_id == recipe.id

            print("READ User Favorites: OK")

            recipe_favorites = get_recipe_favorites(
                session,
                recipe.id,
            )

            assert len(recipe_favorites) == 1
            assert recipe_favorites[0].user_id == user.id

            print("READ Recipe Favorites: OK")

            try:
                add_favorite(
                    session,
                    user.id,
                    recipe.id,
                )

                assert False, "Duplicate favorite should not be accepted."

            except ValueError:
                print("Duplicate validation: OK")

            # 8. DELETE
            removed = remove_favorite(
                session,
                user.id,
                recipe.id,
            )

            assert removed is True

            print("DELETE Favorite: OK")

            assert get_favorite(
                session,
                user.id,
                recipe.id,
            ) is None

            print("Favorite deletion verification: OK")

            print("\nAll Favorite CRUD tests passed!")

        finally:
            session.rollback()
            print("Test transaction rolled back.")


if __name__ == "__main__":
    test_favorite_crud()