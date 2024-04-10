# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Tuple
from geopy.distance import geodesic
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import Info
from fastapi.openapi.utils import get_openapi

from models import Address, AddressCreate
from crud import get_db, create_address, get_address, update_address, delete_address, AddressDB

app = FastAPI()

def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Address Book API",
        version="1.0.0",
        description="API for managing addresses",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> str:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API documentation",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi() -> dict:
    return custom_openapi()

@app.post("/addresses/", response_model=Address)
def create_new_address(address: AddressCreate, db: Session = Depends(get_db)) -> Address:
    """
    Create a new address.

    Args:
        address (AddressCreate): The data of the new address to be created.

    Returns:
        Address: The newly created address.
    """
    try:
        return create_address(db, address)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="Address already exists")

@app.get("/addresses/{address_id}", response_model=Address)
def read_address(address_id: int, db: Session = Depends(get_db)) -> Address:
    """
    Get details of a specific address.

    Args:
        address_id (int): The ID of the address to retrieve.

    Returns:
        Address: Details of the address.
    """
    db_address = get_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=Address)
def update_existing_address(address_id: int, address: AddressCreate, db: Session = Depends(get_db)) -> Address:
    """
    Update an existing address.

    Args:
        address_id (int): The ID of the address to update.
        address (AddressCreate): The updated data for the address.

    Returns:
        Address: The updated address.
    """
    db_address = update_address(db, address_id, address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.delete("/addresses/{address_id}", response_model=Address)
def delete_existing_address(address_id: int, db: Session = Depends(get_db)) -> Address:
    """
    Delete an existing address.

    Args:
        address_id (int): The ID of the address to delete.

    Returns:
        Address: The deleted address.
    """
    db_address = delete_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.get("/addresses/", response_model=List[Address])
def read_addresses_within_distance(latitude: float, longitude: float, distance: float = 10, db: Session = Depends(get_db)) -> List[Address]:
    """
    Get addresses within a specified distance from a given location.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        distance (float, optional): Maximum distance in miles (default is 10).

    Returns:
        List[Address]: List of addresses within the specified distance from the given location.
    """
    addresses: List[Address] = []
    user_location: Tuple[float, float] = (latitude, longitude)
    all_addresses: List[AddressDB] = db.query(AddressDB).all()
    for db_address in all_addresses:
        address_location: Tuple[float, float] = (db_address.latitude, db_address.longitude)
        if geodesic(user_location, address_location).miles <= distance:
            addresses.append(db_address)
    return addresses
