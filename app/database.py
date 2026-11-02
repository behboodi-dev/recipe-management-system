"""
Database connection module.

Establishes a connection to the PostgreSQL database using SQLAlchemy.
Reads credentials from environment variables and creates the main engine.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST", "localhost"),
    port=int(os.getenv("DATABASE_PORT", "5432")),
    database=os.getenv("DATABASE_NAME"),
)

engine = create_engine(database_url)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print("Test result:", result.scalar())

    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)


if __name__ == "__main__":
    test_connection()
