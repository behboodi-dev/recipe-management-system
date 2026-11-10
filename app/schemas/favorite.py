"""
Pydantic schemas for Favorite API operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteCreate(BaseModel):
    """
    Schema for validating data when adding a recipe to favorites.
    """
    recipe_id: int


class FavoriteRead(BaseModel):
    """
    Schema for returning favorite data in API responses.
    """
    user_id: int
    recipe_id: int
    created_at: datetime

    # Allows Pydantic to read data directly from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)