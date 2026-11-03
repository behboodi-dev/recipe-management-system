
"""
Tests for the UserProfile model.

Verifies that the UserProfile table is mapped correctly
and can communicate with the database.
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User, UserProfile, Recipe, Favorite


def test_read_user_profiles():
    """Test reading user profiles from the database."""

    with SessionLocal() as session:

        statement = select(UserProfile).limit(5)

        profiles = session.scalars(statement).all()

        # Check query result
        assert isinstance(profiles, list)

        # Check each profile
        for profile in profiles:
            assert isinstance(profile, UserProfile)
            assert profile.user_id is not None

        print("Successfully queried the user_profiles table.")
        print(f"Found {len(profiles)} profile(s).")


def test_user_profile_table_structure():
    """Test the UserProfile table structure."""

    columns = UserProfile.__table__.c

    assert UserProfile.__tablename__ == "user_profiles"

    assert columns.user_id.primary_key is True
    assert columns.user_id.nullable is False

if __name__ == "__main__":
    test_read_user_profiles()
    test_user_profile_table_structure()
    print("All UserProfile model tests passed!")