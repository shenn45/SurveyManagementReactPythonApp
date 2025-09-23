from fastapi import APIRouter, HTTPException
from typing import List, Optional
import crud
import schemas

router = APIRouter(prefix="/townships", tags=["townships"])

@router.get("/", response_model=schemas.PaginatedResponse[schemas.Township])
def read_townships(skip: int = 0, limit: int = 100, search: Optional[str] = None):
    """Get townships with pagination and optional search"""
    townships, total = crud.get_townships(skip=skip, limit=limit, search=search)
    return schemas.PaginatedResponse(
        data=townships,
        total=total,
        page=(skip // limit) + 1,
        size=limit
    )

@router.get("/{township_id}", response_model=schemas.Township)
def read_township(township_id: str):
    """Get a single township by ID"""
    township = crud.get_township(township_id=township_id)
    if township is None:
        raise HTTPException(status_code=404, detail="Township not found")
    return township

@router.post("/", response_model=schemas.Township)
def create_township(township: schemas.TownshipCreate):
    """Create a new township"""
    db_township = crud.create_township(township=township)
    if db_township is None:
        raise HTTPException(status_code=400, detail="Failed to create township")
    return db_township

@router.put("/{township_id}", response_model=schemas.Township)
def update_township(township_id: str, township: schemas.TownshipUpdate):
    """Update an existing township"""
    db_township = crud.update_township(township_id=township_id, township=township)
    if db_township is None:
        raise HTTPException(status_code=404, detail="Township not found")
    return db_township

@router.delete("/{township_id}")
def delete_township(township_id: str):
    """Delete a township (soft delete)"""
    success = crud.delete_township(township_id=township_id)
    if not success:
        raise HTTPException(status_code=404, detail="Township not found")
    return {"message": "Township deleted successfully"}