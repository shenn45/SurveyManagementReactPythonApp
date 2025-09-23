from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import crud
import schemas

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=schemas.CustomerListResponse)
def read_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None)
):
    customers, total = crud.get_customers(skip=skip, limit=limit, search=search)
    return {
        "customers": customers,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: str):  # Changed from int to str
    db_customer = crud.get_customer(customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate):
    result = crud.create_customer(customer=customer)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create customer")
    return result

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: str,  # Changed from int to str
    customer: schemas.CustomerUpdate
):
    db_customer = crud.update_customer(customer_id=customer_id, customer=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: str):  # Changed from int to str
    success = crud.delete_customer(customer_id=customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}
