from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model=schemas.PropertyListResponse)
def read_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    properties, total = crud.get_properties(db, skip=skip, limit=limit, search=search)
    return {
        "properties": properties,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{property_id}", response_model=schemas.Property)
def read_property(property_id: int, db: Session = Depends(get_db)):
    db_property = crud.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@router.post("/", response_model=schemas.Property)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    return crud.create_property(db=db, property=property)

@router.put("/{property_id}", response_model=schemas.Property)
def update_property(
    property_id: int,
    property: schemas.PropertyUpdate,
    db: Session = Depends(get_db)
):
    db_property = crud.update_property(db, property_id=property_id, property=property)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@router.delete("/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = crud.delete_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Property deleted successfully"}
