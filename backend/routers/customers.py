from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=schemas.CustomerListResponse)
def read_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    customers, total = crud.get_customers(db, skip=skip, limit=limit, search=search)
    return {
        "customers": customers,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(get_db)
):
    db_customer = crud.update_customer(db, customer_id=customer_id, customer=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}
