"""
FastAPI dependencies.

Provides shared dependencies for API routes, such as database sessions.
"""

from app.database import SessionLocal


def get_db():
    """
    Dependency function that provides a database session per request.

    Yields:
        Session: A SQLAlchemy database session.

    Ensures the session is properly closed after the request is finished,
    even if an exception occurs during the request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()