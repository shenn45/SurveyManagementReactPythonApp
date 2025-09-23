from pydantic import BaseModel, EmailStr
from typing import Optional, List, Generic, TypeVar
from datetime import datetime
from decimal import Decimal

# Generic Pagination Schema
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    size: int

# Address Schemas
class AddressBase(BaseModel):
    AddressType: str
    AddressLine1: str
    AddressLine2: Optional[str] = None
    City: str
    StateCode: str
    ZipCode: str
    County: Optional[str] = None
    Country: Optional[str] = "USA"
    IsActive: bool = True

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    AddressId: int
    CreatedDate: datetime
    
    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    CustomerCode: str
    CompanyName: str
    ContactFirstName: Optional[str] = None
    ContactLastName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    IsActive: bool = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    CustomerId: int
    CreatedDate: datetime
    ModifiedDate: datetime
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    class Config:
        from_attributes = True

# Township Schemas
class TownshipBase(BaseModel):
    TownshipName: str
    County: str
    State: str
    IsActive: Optional[bool] = True

class TownshipCreate(TownshipBase):
    pass

class TownshipUpdate(TownshipBase):
    TownshipName: Optional[str] = None
    County: Optional[str] = None
    State: Optional[str] = None
    IsActive: Optional[bool] = None

class Township(TownshipBase):
    TownshipId: str
    CreatedDate: datetime
    ModifiedDate: datetime
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    class Config:
        from_attributes = True

# Property Schemas
class PropertyBase(BaseModel):
    SurveyPrimaryKey: int
    LegacyTax: Optional[str] = None
    District: Optional[str] = None
    Section: Optional[str] = None
    Block: Optional[str] = None
    Lot: Optional[str] = None
    AddressId: Optional[int] = None
    TownshipId: Optional[int] = None
    PropertyType: Optional[str] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class Property(PropertyBase):
    PropertyId: int
    CreatedDate: datetime
    ModifiedDate: datetime
    address: Optional[Address] = None
    township: Optional[Township] = None
    
    class Config:
        from_attributes = True

# Survey Status Schemas
class SurveyStatusBase(BaseModel):
    StatusCode: str
    StatusName: str
    SortOrder: int = 0
    IsActive: bool = True

class SurveyStatusCreate(SurveyStatusBase):
    pass

class SurveyStatusUpdate(SurveyStatusBase):
    pass

class SurveyStatus(SurveyStatusBase):
    StatusId: int
    
    class Config:
        from_attributes = True

# Survey Type Schemas
class SurveyTypeBase(BaseModel):
    TypeName: str
    TypeDescription: Optional[str] = None
    EstimatedDuration: Optional[int] = None
    BasePrice: Optional[Decimal] = None
    IsActive: bool = True

class SurveyTypeCreate(SurveyTypeBase):
    pass

class SurveyTypeUpdate(SurveyTypeBase):
    pass

class SurveyType(SurveyTypeBase):
    SurveyTypeId: int
    
    class Config:
        from_attributes = True

# Survey Note Schemas
class SurveyNoteBase(BaseModel):
    NoteType: str
    NoteText: str
    IsInternal: bool = False

class SurveyNoteCreate(SurveyNoteBase):
    SurveyId: int

class SurveyNoteUpdate(SurveyNoteBase):
    pass

class SurveyNote(SurveyNoteBase):
    NoteId: int
    SurveyId: int
    CreatedDate: datetime
    CreatedBy: Optional[str] = None
    
    class Config:
        from_attributes = True

# Survey Document Schemas
class SurveyDocumentBase(BaseModel):
    DocumentType: str
    FileName: str
    FilePath: str
    FileSize: Optional[int] = None
    MimeType: Optional[str] = None
    IsMainDocument: bool = False

class SurveyDocumentCreate(SurveyDocumentBase):
    SurveyId: int

class SurveyDocumentUpdate(SurveyDocumentBase):
    pass

class SurveyDocument(SurveyDocumentBase):
    DocumentId: int
    SurveyId: int
    UploadedDate: datetime
    UploadedBy: Optional[str] = None
    
    class Config:
        from_attributes = True

# Survey Schemas
class SurveyBase(BaseModel):
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
    QuotedPrice: Optional[Decimal] = None
    FinalPrice: Optional[Decimal] = None
    IsFieldworkComplete: bool = False
    IsDrawingComplete: bool = False
    IsScanned: bool = False
    IsDelivered: bool = False

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(SurveyBase):
    pass

class Survey(SurveyBase):
    SurveyId: int
    CreatedDate: datetime
    ModifiedDate: datetime
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    customer: Optional[Customer] = None
    property: Optional[Property] = None
    survey_type: Optional[SurveyType] = None
    status: Optional[SurveyStatus] = None
    notes: List[SurveyNote] = []
    documents: List[SurveyDocument] = []
    
    class Config:
        from_attributes = True

# Response schemas for lists
class SurveyListResponse(BaseModel):
    surveys: List[Survey]
    total: int
    page: int
    size: int

class CustomerListResponse(BaseModel):
    customers: List[Customer]
    total: int
    page: int
    size: int

class PropertyListResponse(BaseModel):
    properties: List[Property]
    total: int
    page: int
    size: int
