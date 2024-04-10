from typing import Optional
import pydantic

class AddressBase(pydantic.BaseModel):
    """
    Base model for address data.
    """
    latitude: float = pydantic.Field(..., ge=-90, le=90, description="Latitude of the address")
    longitude: float = pydantic.Field(..., ge=-180, le=180, description="Longitude of the address")
    street: str = pydantic.Field(..., min_length=3, description="Street address")
    city: str = pydantic.Field(..., min_length=2, description="City name")

class AddressCreate(AddressBase):
    """
    Model for creating a new address.
    """
    pass

class Address(AddressBase):
    """
    Model representing an address with an ID.
    """
    id: int

    class Config:
        """
        Configuration for the Address model.
        """
        orm_mode = True
