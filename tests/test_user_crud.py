
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import engine
from app.models import User, Recipe, UserProfile, Favorite

from app.services.user import (
    create_user,
    get_user,
    get_users,
    update_user,
    soft_delete_user,
)


def test_user_crud():
    """
    Test the complete User CRUD lifecycle.

    Note:
        A user created with a phone_number must also have a phone_verified_at
        to satisfy the database CHECK constraint (both NULL or both populated).
    """

    with Session(engine) as session:
        try:
           
            user = create_user(
                session=session,
                phone_number="+989121234567",
                phone_verified_at=datetime.now(timezone.utc)
            )

            assert user.id is not None
            assert user.phone_number == "+989121234567"

            print("CREATE User: OK")

         
            found_user = get_user(session, user.id)

            assert found_user is not None
            assert found_user.id == user.id

            print("READ User: OK")

            
            users = get_users(session)

            assert any(item.id == user.id for item in users)

            print("READ Users: OK")

            
            new_phone = "+989121234568"

            updated_user = update_user(
                session,
                user.id,
                phone_number=new_phone,
                phone_verified_at=datetime.now(timezone.utc),
            )

            assert updated_user.phone_number == new_phone
            assert updated_user.phone_verified_at is not None

            print("UPDATE User: OK")

            # 5. Prepare related records for soft-delete test
            profile = UserProfile(
                user_id=user.id,
                username="test_user_crud",
            )

            session.add(profile)

            recipe = Recipe(
                user_id=user.id,
                title="User Test Recipe",
                prep_time_minutes=10,
                cook_time_minutes=20,
                servings=2,
            )

            session.add(recipe)
            session.flush()

            favorite = Favorite(
                user_id=user.id,
                recipe_id=recipe.id,
            )

            session.add(favorite)
            session.flush()

            # 6. SOFT DELETE
            deleted = soft_delete_user(session, user.id)

            assert deleted is True

            print("SOFT DELETE User: OK")

            # 7. Verify soft-delete behavior
            session.expire_all()

            assert get_user(session, user.id) is None

            deleted_user = session.get(User, user.id)

            assert deleted_user is not None
            assert deleted_user.deleted_at is not None
            assert deleted_user.phone_number is None
            assert deleted_user.phone_verified_at is None

            assert session.get(UserProfile, user.id) is None

            remaining_favorite = session.get(
                Favorite,
                (user.id, recipe.id),
            )

            assert remaining_favorite is None

            # Recipe must remain
            remaining_recipe = session.get(Recipe, recipe.id)

            assert remaining_recipe is not None

            print("Soft-delete rules: OK")

            print("\nAll User CRUD tests passed!")

        finally:
            session.rollback()
            print("Test transaction rolled back.")


if __name__ == "__main__":
    test_user_crud()
