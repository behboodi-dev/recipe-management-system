"""
Pydantic schemas for User and Authentication API operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OTPRequest(BaseModel):
    """
    Schema for receiving a phone number to initiate the OTP process.
    
    This does not create a user record; it only triggers the OTP flow.
    """
    phone_number: str = Field(
        min_length=11,
        max_length=20,
    )


class UserRead(BaseModel):
    """
    Schema for returning verified user data in API responses.
    """
    id: int
    phone_number: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)