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

class CustomerUpdate(BaseModel):
    CustomerCode: Optional[str] = None
    CompanyName: Optional[str] = None
    ContactFirstName: Optional[str] = None
    ContactLastName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    IsActive: Optional[bool] = None

class Customer(CustomerBase):
    CustomerId: str  # Changed from int to str for UUID consistency
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
    PropertyCode: Optional[str] = None
    PropertyName: Optional[str] = None
    PropertyDescription: Optional[str] = None
    OwnerName: Optional[str] = None
    OwnerPhone: Optional[str] = None
    OwnerEmail: Optional[str] = None
    SurveyPrimaryKey: Optional[int] = None  # Make optional for updates
    LegacyTax: Optional[str] = None
    District: Optional[str] = None
    Section: Optional[str] = None
    Block: Optional[str] = None
    Lot: Optional[str] = None
    AddressId: Optional[str] = None  # Changed from int to str for UUID
    TownshipId: Optional[str] = None  # Changed from int to str for UUID
    PropertyType: Optional[str] = None
    IsActive: Optional[bool] = True

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class Property(PropertyBase):
    PropertyId: str  # Changed from int to str for UUID
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

class SurveyStatusUpdate(BaseModel):
    StatusCode: Optional[str] = None
    StatusName: Optional[str] = None
    SortOrder: Optional[int] = None
    IsActive: Optional[bool] = None

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
    CustomerId: Optional[str] = None
    PropertyId: Optional[str] = None
    SurveyTypeId: Optional[str] = None
    StatusId: Optional[str] = None
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
    EstimatedCost: Optional[Decimal] = None
    ActualCost: Optional[Decimal] = None
    Notes: Optional[str] = None
    IsFieldworkComplete: bool = False
    IsDrawingComplete: bool = False
    IsScanned: bool = False
    IsDelivered: bool = False

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(BaseModel):
    SurveyNumber: Optional[str] = None
    CustomerId: Optional[str] = None
    PropertyId: Optional[str] = None
    SurveyTypeId: Optional[str] = None
    StatusId: Optional[str] = None
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
    EstimatedCost: Optional[Decimal] = None
    ActualCost: Optional[Decimal] = None
    Notes: Optional[str] = None
    IsFieldworkComplete: Optional[bool] = None
    IsDrawingComplete: Optional[bool] = None
    IsScanned: Optional[bool] = None
    IsDelivered: Optional[bool] = None

class Survey(SurveyBase):
    SurveyId: str
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

# UserSettings Schemas
class UserSettingsBase(BaseModel):
    UserId: str
    SettingsType: str
    SettingsData: dict
    IsActive: bool = True

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettingsUpdate(BaseModel):
    SettingsData: Optional[dict] = None
    IsActive: Optional[bool] = None

class UserSettings(UserSettingsBase):
    UserSettingsId: str
    CreatedDate: datetime
    ModifiedDate: datetime
    
    class Config:
        from_attributes = True

# Board Configuration Schemas
class BoardConfigurationBase(BaseModel):
    BoardName: str
    Description: Optional[str] = None
    UserId: Optional[str] = None
    IsDefault: bool = False
    IsActive: bool = True

class BoardConfigurationCreate(BoardConfigurationBase):
    pass

class BoardConfigurationUpdate(BaseModel):
    BoardName: Optional[str] = None
    Description: Optional[str] = None
    IsDefault: Optional[bool] = None
    IsActive: Optional[bool] = None

class BoardConfiguration(BoardConfigurationBase):
    BoardConfigId: str
    BoardSlug: str
    CreatedDate: datetime
    ModifiedDate: datetime
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    class Config:
        from_attributes = True

class BoardConfigurationListResponse(BaseModel):
    board_configurations: List[BoardConfiguration]
    total: int
    page: int
    size: int
