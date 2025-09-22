import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

import crud
from database import get_db
from sqlalchemy.orm import Session


# GraphQL Types
@strawberry.type
class Customer:
    CustomerId: int
    CustomerCode: str
    CompanyName: str
    ContactFirstName: Optional[str] = None
    ContactLastName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    IsActive: bool
    CreatedDate: datetime
    ModifiedDate: datetime
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None

@strawberry.type
class Survey:
    SurveyId: int
    SurveyNumber: str
    CustomerId: Optional[int] = None
    PropertyId: Optional[int] = None
    SurveyTypeId: Optional[int] = None
    StatusId: int
    Title: Optional[str] = None
    Description: Optional[str] = None
    PurposeCode: Optional[str] = None
    RequestDate: Optional[datetime] = None
    ScheduledDate: Optional[datetime] = None
    CompletedDate: Optional[datetime] = None
    DeliveryDate: Optional[datetime] = None
    DueDate: Optional[datetime] = None
    QuotedPrice: Optional[float] = None
    FinalPrice: Optional[float] = None
    IsFieldworkComplete: bool
    IsDrawingComplete: bool
    IsScanned: bool
    IsDelivered: bool
    CreatedDate: datetime
    ModifiedDate: datetime
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None

@strawberry.type
class Property:
    PropertyId: int
    SurveyPrimaryKey: int
    LegacyTax: Optional[str] = None
    District: Optional[str] = None
    Section: Optional[str] = None
    Block: Optional[str] = None
    Lot: Optional[str] = None
    AddressId: Optional[int] = None
    TownshipId: Optional[int] = None
    PropertyType: Optional[str] = None
    CreatedDate: datetime
    ModifiedDate: datetime

@strawberry.type
class SurveyType:
    SurveyTypeId: int
    TypeName: str
    TypeDescription: Optional[str] = None
    EstimatedDuration: Optional[int] = None
    BasePrice: Optional[float] = None
    IsActive: bool

@strawberry.type
class SurveyStatus:
    StatusId: int
    StatusCode: str
    StatusName: str
    SortOrder: int
    IsActive: bool

@strawberry.type
class Township:
    TownshipId: int
    Name: str
    FoilMethod: Optional[str] = None
    Website: Optional[str] = None
    Description: Optional[str] = None


# Response Types for Pagination
@strawberry.type
class CustomerListResponse:
    customers: List[Customer]
    total: int
    page: int
    size: int

@strawberry.type
class SurveyListResponse:
    surveys: List[Survey]
    total: int
    page: int
    size: int

@strawberry.type
class PropertyListResponse:
    properties: List[Property]
    total: int
    page: int
    size: int


# Input Types for Mutations
@strawberry.input
class CustomerInput:
    CustomerCode: str
    CompanyName: str
    ContactFirstName: Optional[str] = None
    ContactLastName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    IsActive: bool = True

@strawberry.input
class CustomerUpdateInput:
    CustomerCode: Optional[str] = None
    CompanyName: Optional[str] = None
    ContactFirstName: Optional[str] = None
    ContactLastName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    IsActive: Optional[bool] = None

@strawberry.input
class SurveyInput:
    SurveyNumber: str
    CustomerId: Optional[int] = None
    PropertyId: Optional[int] = None
    SurveyTypeId: Optional[int] = None
    StatusId: int
    Title: Optional[str] = None
    Description: Optional[str] = None
    PurposeCode: Optional[str] = None
    RequestDate: Optional[datetime] = None
    ScheduledDate: Optional[datetime] = None
    CompletedDate: Optional[datetime] = None
    DeliveryDate: Optional[datetime] = None
    DueDate: Optional[datetime] = None
    QuotedPrice: Optional[float] = None
    FinalPrice: Optional[float] = None
    IsFieldworkComplete: bool = False
    IsDrawingComplete: bool = False
    IsScanned: bool = False
    IsDelivered: bool = False

@strawberry.input
class SurveyUpdateInput:
    SurveyNumber: Optional[str] = None
    CustomerId: Optional[int] = None
    PropertyId: Optional[int] = None
    SurveyTypeId: Optional[int] = None
    StatusId: Optional[int] = None
    Title: Optional[str] = None
    Description: Optional[str] = None
    PurposeCode: Optional[str] = None
    RequestDate: Optional[datetime] = None
    ScheduledDate: Optional[datetime] = None
    CompletedDate: Optional[datetime] = None
    DeliveryDate: Optional[datetime] = None
    DueDate: Optional[datetime] = None
    QuotedPrice: Optional[float] = None
    FinalPrice: Optional[float] = None
    IsFieldworkComplete: Optional[bool] = None
    IsDrawingComplete: Optional[bool] = None
    IsScanned: Optional[bool] = None
    IsDelivered: Optional[bool] = None

@strawberry.input
class PropertyInput:
    SurveyPrimaryKey: int
    LegacyTax: Optional[str] = None
    District: Optional[str] = None
    Section: Optional[str] = None
    Block: Optional[str] = None
    Lot: Optional[str] = None
    AddressId: Optional[int] = None
    TownshipId: Optional[int] = None
    PropertyType: Optional[str] = None

@strawberry.input
class PropertyUpdateInput:
    SurveyPrimaryKey: Optional[int] = None
    LegacyTax: Optional[str] = None
    District: Optional[str] = None
    Section: Optional[str] = None
    Block: Optional[str] = None
    Lot: Optional[str] = None
    AddressId: Optional[int] = None
    TownshipId: Optional[int] = None
    PropertyType: Optional[str] = None


# Utility function to get database session
def get_db_session():
    return next(get_db())


# Convert model to GraphQL type
def model_to_customer(customer_model) -> Customer:
    return Customer(
        CustomerId=customer_model.CustomerId,
        CustomerCode=customer_model.CustomerCode,
        CompanyName=customer_model.CompanyName,
        ContactFirstName=customer_model.ContactFirstName,
        ContactLastName=customer_model.ContactLastName,
        Email=customer_model.Email,
        Phone=customer_model.Phone,
        Fax=customer_model.Fax,
        Website=customer_model.Website,
        IsActive=customer_model.IsActive,
        CreatedDate=customer_model.CreatedDate,
        ModifiedDate=customer_model.ModifiedDate,
        CreatedBy=customer_model.CreatedBy,
        ModifiedBy=customer_model.ModifiedBy
    )

def model_to_survey(survey_model) -> Survey:
    return Survey(
        SurveyId=survey_model.SurveyId,
        SurveyNumber=survey_model.SurveyNumber,
        CustomerId=survey_model.CustomerId,
        PropertyId=survey_model.PropertyId,
        SurveyTypeId=survey_model.SurveyTypeId,
        StatusId=survey_model.StatusId,
        Title=survey_model.Title,
        Description=survey_model.Description,
        PurposeCode=survey_model.PurposeCode,
        RequestDate=survey_model.RequestDate,
        ScheduledDate=survey_model.ScheduledDate,
        CompletedDate=survey_model.CompletedDate,
        DeliveryDate=survey_model.DeliveryDate,
        DueDate=survey_model.DueDate,
        QuotedPrice=float(survey_model.QuotedPrice) if survey_model.QuotedPrice else None,
        FinalPrice=float(survey_model.FinalPrice) if survey_model.FinalPrice else None,
        IsFieldworkComplete=survey_model.IsFieldworkComplete,
        IsDrawingComplete=survey_model.IsDrawingComplete,
        IsScanned=survey_model.IsScanned,
        IsDelivered=survey_model.IsDelivered,
        CreatedDate=survey_model.CreatedDate,
        ModifiedDate=survey_model.ModifiedDate,
        CreatedBy=survey_model.CreatedBy,
        ModifiedBy=survey_model.ModifiedBy
    )

def model_to_property(property_model) -> Property:
    return Property(
        PropertyId=property_model.PropertyId,
        SurveyPrimaryKey=property_model.SurveyPrimaryKey,
        LegacyTax=property_model.LegacyTax,
        District=property_model.District,
        Section=property_model.Section,
        Block=property_model.Block,
        Lot=property_model.Lot,
        AddressId=property_model.AddressId,
        TownshipId=property_model.TownshipId,
        PropertyType=property_model.PropertyType,
        CreatedDate=property_model.CreatedDate,
        ModifiedDate=property_model.ModifiedDate
    )

def model_to_survey_type(survey_type_model) -> SurveyType:
    return SurveyType(
        SurveyTypeId=survey_type_model.SurveyTypeId,
        TypeName=survey_type_model.TypeName,
        TypeDescription=survey_type_model.TypeDescription,
        EstimatedDuration=survey_type_model.EstimatedDuration,
        BasePrice=float(survey_type_model.BasePrice) if survey_type_model.BasePrice else None,
        IsActive=survey_type_model.IsActive
    )

def model_to_survey_status(survey_status_model) -> SurveyStatus:
    return SurveyStatus(
        StatusId=survey_status_model.StatusId,
        StatusCode=survey_status_model.StatusCode,
        StatusName=survey_status_model.StatusName,
        SortOrder=survey_status_model.SortOrder,
        IsActive=survey_status_model.IsActive
    )

def model_to_township(township_model) -> Township:
    return Township(
        TownshipId=township_model.TownshipId,
        Name=township_model.Name,
        FoilMethod=township_model.FoilMethod,
        Website=township_model.Website,
        Description=township_model.Description
    )


@strawberry.type
class Query:
    @strawberry.field
    def customers(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> CustomerListResponse:
        db = get_db_session()
        try:
            customers_data, total = crud.get_customers(db, skip=skip, limit=limit, search=search)
            customers = [model_to_customer(c) for c in customers_data]
            return CustomerListResponse(
                customers=customers,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        finally:
            db.close()

    @strawberry.field
    def customer(self, customer_id: int) -> Optional[Customer]:
        db = get_db_session()
        try:
            customer_data = crud.get_customer(db, customer_id=customer_id)
            return model_to_customer(customer_data) if customer_data else None
        finally:
            db.close()

    @strawberry.field
    def surveys(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> SurveyListResponse:
        db = get_db_session()
        try:
            surveys_data, total = crud.get_surveys(db, skip=skip, limit=limit, search=search)
            surveys = [model_to_survey(s) for s in surveys_data]
            return SurveyListResponse(
                surveys=surveys,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        finally:
            db.close()

    @strawberry.field
    def survey(self, survey_id: int) -> Optional[Survey]:
        db = get_db_session()
        try:
            survey_data = crud.get_survey(db, survey_id=survey_id)
            return model_to_survey(survey_data) if survey_data else None
        finally:
            db.close()

    @strawberry.field
    def properties(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> PropertyListResponse:
        db = get_db_session()
        try:
            properties_data, total = crud.get_properties(db, skip=skip, limit=limit, search=search)
            properties = [model_to_property(p) for p in properties_data]
            return PropertyListResponse(
                properties=properties,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        finally:
            db.close()

    @strawberry.field
    def property(self, property_id: int) -> Optional[Property]:
        db = get_db_session()
        try:
            property_data = crud.get_property(db, property_id=property_id)
            return model_to_property(property_data) if property_data else None
        finally:
            db.close()

    @strawberry.field
    def survey_types(self) -> List[SurveyType]:
        db = get_db_session()
        try:
            survey_types_data = crud.get_survey_types(db)
            return [model_to_survey_type(st) for st in survey_types_data]
        finally:
            db.close()

    @strawberry.field
    def survey_statuses(self) -> List[SurveyStatus]:
        db = get_db_session()
        try:
            survey_statuses_data = crud.get_survey_statuses(db)
            return [model_to_survey_status(ss) for ss in survey_statuses_data]
        finally:
            db.close()

    @strawberry.field
    def townships(self) -> List[Township]:
        db = get_db_session()
        try:
            townships_data = crud.get_townships(db)
            return [model_to_township(t) for t in townships_data]
        finally:
            db.close()


@strawberry.type
class Mutation:
    @strawberry.field
    def create_customer(self, input: CustomerInput) -> Customer:
        db = get_db_session()
        try:
            from schemas import CustomerCreate
            customer_data = CustomerCreate(**strawberry.asdict(input))
            customer = crud.create_customer(db=db, customer=customer_data)
            return model_to_customer(customer)
        finally:
            db.close()

    @strawberry.field
    def update_customer(self, customer_id: int, input: CustomerUpdateInput) -> Optional[Customer]:
        db = get_db_session()
        try:
            from schemas import CustomerUpdate
            # Filter out None values
            update_data = {k: v for k, v in strawberry.asdict(input).items() if v is not None}
            customer_data = CustomerUpdate(**update_data)
            customer = crud.update_customer(db=db, customer_id=customer_id, customer=customer_data)
            return model_to_customer(customer) if customer else None
        finally:
            db.close()

    @strawberry.field
    def delete_customer(self, customer_id: int) -> bool:
        db = get_db_session()
        try:
            customer = crud.delete_customer(db=db, customer_id=customer_id)
            return customer is not None
        finally:
            db.close()

    @strawberry.field
    def create_survey(self, input: SurveyInput) -> Survey:
        db = get_db_session()
        try:
            from schemas import SurveyCreate
            survey_data = SurveyCreate(**strawberry.asdict(input))
            survey = crud.create_survey(db=db, survey=survey_data)
            return model_to_survey(survey)
        finally:
            db.close()

    @strawberry.field
    def update_survey(self, survey_id: int, input: SurveyUpdateInput) -> Optional[Survey]:
        db = get_db_session()
        try:
            from schemas import SurveyUpdate
            # Filter out None values
            update_data = {k: v for k, v in strawberry.asdict(input).items() if v is not None}
            survey_data = SurveyUpdate(**update_data)
            survey = crud.update_survey(db=db, survey_id=survey_id, survey=survey_data)
            return model_to_survey(survey) if survey else None
        finally:
            db.close()

    @strawberry.field
    def delete_survey(self, survey_id: int) -> bool:
        db = get_db_session()
        try:
            survey = crud.delete_survey(db=db, survey_id=survey_id)
            return survey is not None
        finally:
            db.close()

    @strawberry.field
    def create_property(self, input: PropertyInput) -> Property:
        db = get_db_session()
        try:
            from schemas import PropertyCreate
            property_data = PropertyCreate(**strawberry.asdict(input))
            property = crud.create_property(db=db, property=property_data)
            return model_to_property(property)
        finally:
            db.close()

    @strawberry.field
    def update_property(self, property_id: int, input: PropertyUpdateInput) -> Optional[Property]:
        db = get_db_session()
        try:
            from schemas import PropertyUpdate
            # Filter out None values
            update_data = {k: v for k, v in strawberry.asdict(input).items() if v is not None}
            property_data = PropertyUpdate(**update_data)
            property = crud.update_property(db=db, property_id=property_id, property=property_data)
            return model_to_property(property) if property else None
        finally:
            db.close()

    @strawberry.field
    def delete_property(self, property_id: int) -> bool:
        db = get_db_session()
        try:
            property = crud.delete_property(db=db, property_id=property_id)
            return property is not None
        finally:
            db.close()


# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
