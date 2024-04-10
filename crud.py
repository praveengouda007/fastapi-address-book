from models import AddressCreate
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./addresses.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AddressDB(Base):
    """
    Database model for storing address information.
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    street = Column(String)
    city = Column(String)

def get_db() -> Session:
    """
    Dependency to get a database session.

    Returns:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_address(db: Session, address: AddressCreate) -> AddressDB:
    """
    Create a new address.

    Args:
        db (Session): Database session.
        address (AddressCreate): Data of the new address to be created.

    Returns:
        AddressDB: Newly created address.
    """
    db_address = AddressDB(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int) -> AddressDB:
    """
    Get details of a specific address.

    Args:
        db (Session): Database session.
        address_id (int): ID of the address to retrieve.

    Returns:
        AddressDB: Details of the address.
    """
    return db.query(AddressDB).filter(AddressDB.id == address_id).first()

def update_address(db: Session, address_id: int, address: AddressCreate) -> AddressDB:
    """
    Update an existing address.

    Args:
        db (Session): Database session.
        address_id (int): ID of the address to update.
        address (AddressCreate): Updated data for the address.

    Returns:
        AddressDB: Updated address.
    """
    db_address = db.query(AddressDB).filter(AddressDB.id == address_id).first()
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int) -> AddressDB:
    """
    Delete an existing address.

    Args:
        db (Session): Database session.
        address_id (int): ID of the address to delete.

    Returns:
        AddressDB: Deleted address.
    """
    db_address = db.query(AddressDB).filter(AddressDB.id == address_id).first()
    db.delete(db_address)
    db.commit()
    return db_address
