# """
# FastAPI dependencies.

# Provides shared dependencies for API routes, such as database sessions.
# """

# from app.database import SessionLocal


# def get_db():
#     """
#     Dependency function that provides a database session per request.

#     Yields:
#         Session: A SQLAlchemy database session.

#     Ensures the session is properly closed after the request is finished,
#     even if an exception occurs during the request handling.
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


"""
FastAPI dependencies.

Provides shared dependencies for API routes, such as database sessions
and the current authenticated user.
"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session per request.

    Yields:
        Session: A SQLAlchemy database session.

    Ensures the session is properly closed after the request is finished,
    even if an exception occurs during request handling.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    x_user_id: Annotated[int, Header(alias="X-User-ID")],
    db: DbSession,
) -> User:
    """
    Dependency function to retrieve the current authenticated user.

    This is a temporary implementation that reads the user ID from the
    'X-User-ID' header instead of using a full authentication system.

    Args:
        x_user_id (int): The user ID passed in the request header.
        db (Session): The database session.

    Raises:
        HTTPException: 401 Unauthorized if the user does not exist
                       or has been soft-deleted.

    Returns:
        User: The active user object.
    """
    user = db.get(User, x_user_id)

    if user is None or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive user.",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]