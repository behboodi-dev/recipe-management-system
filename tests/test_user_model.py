
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import User


def test_user_model():
    with Session(engine) as session:
        users = session.scalars(
            select(User).order_by(User.id)
        ).all()

        print("User model works successfully!")
        print("Number of users:", len(users))

        for user in users:
            print("User ID:", user.id)


if __name__ == "__main__":
    test_user_model()
