"""
Database connection module.

Establishes a connection to PostgreSQL using SQLAlchemy.
Reads database credentials from environment variables.
Creates the database engine and session factory.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()


database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")
database_host = os.getenv("DATABASE_HOST", "localhost")
database_name = os.getenv("DATABASE_NAME")

if not all([database_user, database_password, database_name]):
    raise ValueError(
        "Database configuration is incomplete. "
        "Check DATABASE_USER, DATABASE_PASSWORD, and DATABASE_NAME."
    )


try:
    database_port = int(os.getenv("DATABASE_PORT", "5432"))
except ValueError:
    raise ValueError("DATABASE_PORT must be a valid integer.")


database_url = URL.create(
    drivername="postgresql+psycopg",
    username=database_user,
    password=database_password,
    host=database_host,
    port=database_port,
    database=database_name,
)


engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)


def test_connection():
    """Test the connection to the PostgreSQL database."""

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        value = result.scalar_one()

        print("Database connection successful!")
        print("Test result:", value)

        return value == 1


if __name__ == "__main__":

    try:
        test_connection()

    except SQLAlchemyError as error:
        print("Database connection failed!")
        print("Error:", error)
        raise SystemExit(1)
