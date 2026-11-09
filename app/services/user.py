from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User, Favorite


def create_user(
    session: Session,
    phone_number: str | None = None,
    phone_verified_at: datetime | None = None,
) -> User:
    """Create a new user, validating phone verification rules."""
    
    if phone_number is None and phone_verified_at is not None:
        raise ValueError("Phone verification time requires a phone number.")

    if phone_number is not None and not phone_number.strip():
        raise ValueError("Phone number cannot be empty.")

    user = User(
        phone_number=phone_number,
        phone_verified_at=phone_verified_at,
    )

    session.add(user)
    session.flush()
    return user


def get_user(session: Session, user_id: int) -> User | None:
    """Retrieve an active user by their ID."""
    
    statement = select(User).where(
        User.id == user_id,
        User.deleted_at.is_(None),
    )
    return session.scalars(statement).first()


def get_users(
    session: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[User]:
    """Retrieve a paginated list of active users."""
    
    if offset < 0:
        raise ValueError("Offset cannot be negative.")
    if limit <= 0:
        raise ValueError("Limit must be positive.")

    statement = (
        select(User)
        .where(User.deleted_at.is_(None))
        .order_by(User.created_at.desc(), User.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(session.scalars(statement).all())


def update_user(
    session: Session,
    user_id: int,
    **updates,
) -> User | None:
    """Update an active user's phone information with validation."""
    
    allowed_fields = {"phone_number", "phone_verified_at"}

    if not updates:
        raise ValueError("At least one field is required.")

    invalid_fields = set(updates) - allowed_fields
    if invalid_fields:
        raise ValueError(f"Fields cannot be updated: {', '.join(sorted(invalid_fields))}")

    if "phone_number" in updates:
        phone_number = updates["phone_number"]
        if phone_number is not None:
            if not isinstance(phone_number, str) or not phone_number.strip():
                raise ValueError("Phone number cannot be empty.")
            updates["phone_number"] = phone_number.strip()

    if "phone_verified_at" in updates:
        verified_at = updates["phone_verified_at"]
        if verified_at is not None and not isinstance(verified_at, datetime):
            raise ValueError("phone_verified_at must be a datetime.")

    user = get_user(session, user_id)
    if user is None:
        return None

    for field, value in updates.items():
        setattr(user, field, value)

    session.flush()
    return user


def soft_delete_user(session: Session, user_id: int) -> bool:
    """Soft-delete a user, removing their profile and favorites."""
    
    user = get_user(session, user_id)
    if user is None:
        return False

    session.query(Favorite).filter(Favorite.user_id == user_id).delete(synchronize_session=False)

    if user.profile is not None:
        session.delete(user.profile)

    user.phone_number = None
    user.phone_verified_at = None
    user.deleted_at = datetime.now(timezone.utc)
    
    session.flush()
    return True