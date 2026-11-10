"""
Pydantic schemas for Recipe API operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    """
    Schema for validating data when creating a new recipe.
    
    Enforces that preparation/cooking times are >= 0 and servings > 0.
    """
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    prep_time_minutes: int = Field(
        ge=0,
    )

    cook_time_minutes: int = Field(
        ge=0,
    )

    servings: int = Field(
        gt=0,
    )

    image_url: str | None = None


class RecipeRead(BaseModel):
    """
    Schema for returning recipe data in API responses.
    
    Includes database-generated fields (id, user_id, timestamps).
    """
    id: int
    user_id: int

    title: str
    description: str | None

    prep_time_minutes: int
    cook_time_minutes: int
    servings: int

    image_url: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)