from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from models import *
import schemas

# Customer CRUD
def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.CustomerId == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Customer)
    
    if search:
        query = query.filter(
            or_(
                Customer.CompanyName.contains(search),
                Customer.CustomerCode.contains(search),
                Customer.Email.contains(search)
            )
        )
    
    total = query.count()
    customers = query.offset(skip).limit(limit).all()
    return customers, total

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = db.query(Customer).filter(Customer.CustomerId == customer_id).first()
    if db_customer:
        for key, value in customer.dict(exclude_unset=True).items():
            setattr(db_customer, key, value)
        db_customer.ModifiedDate = func.utcnow()
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.CustomerId == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# Address CRUD
def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.AddressId == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Address)
    
    if search:
        query = query.filter(
            or_(
                Address.AddressLine1.contains(search),
                Address.City.contains(search),
                Address.StateCode.contains(search),
                Address.ZipCode.contains(search)
            )
        )
    
    total = query.count()
    addresses = query.offset(skip).limit(limit).all()
    return addresses, total

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = db.query(Address).filter(Address.AddressId == address_id).first()
    if db_address:
        for key, value in address.dict(exclude_unset=True).items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = db.query(Address).filter(Address.AddressId == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address

# Property CRUD
def get_property(db: Session, property_id: int):
    return db.query(Property).filter(Property.PropertyId == property_id).first()

def get_properties(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Property).join(Address, Property.AddressId == Address.AddressId, isouter=True)
    
    if search:
        query = query.filter(
            or_(
                Property.LegacyTax.contains(search),
                Property.District.contains(search),
                Property.Block.contains(search),
                Property.Lot.contains(search),
                Address.AddressLine1.contains(search),
                Address.City.contains(search)
            )
        )
    
    total = query.count()
    properties = query.offset(skip).limit(limit).all()
    return properties, total

def create_property(db: Session, property: schemas.PropertyCreate):
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, property_id: int, property: schemas.PropertyUpdate):
    db_property = db.query(Property).filter(Property.PropertyId == property_id).first()
    if db_property:
        for key, value in property.dict(exclude_unset=True).items():
            setattr(db_property, key, value)
        db_property.ModifiedDate = func.utcnow()
        db.commit()
        db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int):
    db_property = db.query(Property).filter(Property.PropertyId == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
    return db_property

# Survey CRUD
def get_survey(db: Session, survey_id: int):
    return db.query(Survey).filter(Survey.SurveyId == survey_id).first()

def get_surveys(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(Survey).join(Customer, Survey.CustomerId == Customer.CustomerId, isouter=True)
    
    if search:
        query = query.filter(
            or_(
                Survey.SurveyNumber.contains(search),
                Survey.Title.contains(search),
                Customer.CompanyName.contains(search)
            )
        )
    
    total = query.count()
    surveys = query.offset(skip).limit(limit).all()
    return surveys, total

def create_survey(db: Session, survey: schemas.SurveyCreate):
    db_survey = Survey(**survey.dict())
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def update_survey(db: Session, survey_id: int, survey: schemas.SurveyUpdate):
    db_survey = db.query(Survey).filter(Survey.SurveyId == survey_id).first()
    if db_survey:
        for key, value in survey.dict(exclude_unset=True).items():
            setattr(db_survey, key, value)
        db_survey.ModifiedDate = func.utcnow()
        db.commit()
        db.refresh(db_survey)
    return db_survey

def delete_survey(db: Session, survey_id: int):
    db_survey = db.query(Survey).filter(Survey.SurveyId == survey_id).first()
    if db_survey:
        db.delete(db_survey)
        db.commit()
    return db_survey

# Survey Type CRUD
def get_survey_types(db: Session):
    return db.query(SurveyType).filter(SurveyType.IsActive == True).all()

def create_survey_type(db: Session, survey_type: schemas.SurveyTypeCreate):
    db_survey_type = SurveyType(**survey_type.dict())
    db.add(db_survey_type)
    db.commit()
    db.refresh(db_survey_type)
    return db_survey_type

# Survey Status CRUD
def get_survey_statuses(db: Session):
    return db.query(SurveyStatus).filter(SurveyStatus.IsActive == True).order_by(SurveyStatus.SortOrder).all()

def create_survey_status(db: Session, survey_status: schemas.SurveyStatusCreate):
    db_survey_status = SurveyStatus(**survey_status.dict())
    db.add(db_survey_status)
    db.commit()
    db.refresh(db_survey_status)
    return db_survey_status

# Township CRUD
def get_townships(db: Session):
    return db.query(Township).all()

def create_township(db: Session, township: schemas.TownshipCreate):
    db_township = Township(**township.dict())
    db.add(db_township)
    db.commit()
    db.refresh(db_township)
    return db_township

# Survey Notes CRUD
def get_survey_notes(db: Session, survey_id: int):
    return db.query(SurveyNote).filter(SurveyNote.SurveyId == survey_id).all()

def create_survey_note(db: Session, note: schemas.SurveyNoteCreate):
    db_note = SurveyNote(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_survey_note(db: Session, note_id: int):
    db_note = db.query(SurveyNote).filter(SurveyNote.NoteId == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note

# Survey Documents CRUD
def get_survey_documents(db: Session, survey_id: int):
    return db.query(SurveyDocument).filter(SurveyDocument.SurveyId == survey_id).all()

def create_survey_document(db: Session, document: schemas.SurveyDocumentCreate):
    db_document = SurveyDocument(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_survey_document(db: Session, document_id: int):
    db_document = db.query(SurveyDocument).filter(SurveyDocument.DocumentId == document_id).first()
    if db_document:
        db.delete(db_document)
        db.commit()
    return db_document
