from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, BigInteger, Float, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Address(Base):
    __tablename__ = "Addresses"
    
    AddressId = Column(Integer, primary_key=True, index=True)
    AddressType = Column(String(20), nullable=False)
    AddressLine1 = Column(String(100), nullable=False)
    AddressLine2 = Column(String(255), nullable=True)
    City = Column(String(50), nullable=False)
    StateCode = Column(String(2), nullable=False)
    ZipCode = Column(String(10), nullable=False)
    County = Column(String(100), nullable=True)
    Country = Column(String(100), nullable=True, default="USA")
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=func.utcnow())
    
    # Relationships
    customer_addresses = relationship("CustomerAddress", back_populates="address")
    properties = relationship("Property", back_populates="address")

class Customer(Base):
    __tablename__ = "Customers"
    
    CustomerId = Column(Integer, primary_key=True, index=True)
    CustomerCode = Column(String(20), nullable=False, unique=True)
    CompanyName = Column(String(255), nullable=False, index=True)
    ContactFirstName = Column(String(100), nullable=True)
    ContactLastName = Column(String(100), nullable=True)
    Email = Column(String(255), nullable=True, index=True)
    Phone = Column(String(20), nullable=True)
    Fax = Column(String(20), nullable=True)
    Website = Column(String(255), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=func.utcnow())
    ModifiedDate = Column(DateTime, nullable=False, default=func.utcnow())
    CreatedBy = Column(String(100), nullable=True)
    ModifiedBy = Column(String(100), nullable=True)
    
    # Relationships
    customer_addresses = relationship("CustomerAddress", back_populates="customer")
    surveys = relationship("Survey", back_populates="customer")

class CustomerAddress(Base):
    __tablename__ = "CustomerAddresses"
    
    CustomerAddressId = Column(Integer, primary_key=True, index=True)
    CustomerId = Column(Integer, ForeignKey("Customers.CustomerId"), nullable=False)
    AddressId = Column(Integer, ForeignKey("Addresses.AddressId"), nullable=False)
    IsPrimary = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, default=func.utcnow())
    
    # Relationships
    customer = relationship("Customer", back_populates="customer_addresses")
    address = relationship("Address", back_populates="customer_addresses")

class Township(Base):
    __tablename__ = "Townships"
    
    TownshipId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    FoilMethod = Column(String(255), nullable=True)
    Website = Column(String(1000), nullable=True)
    Description = Column(String(500), nullable=True)
    
    # Relationships
    properties = relationship("Property", back_populates="township")

class Property(Base):
    __tablename__ = "Properties"
    
    PropertyId = Column(Integer, primary_key=True, index=True)
    SurveyPrimaryKey = Column(Integer, nullable=False, unique=True)
    LegacyTax = Column(String(50), nullable=True)
    District = Column(String(10), nullable=True)
    Section = Column(String(10), nullable=True)
    Block = Column(String(50), nullable=True)
    Lot = Column(String(50), nullable=True)
    AddressId = Column(Integer, ForeignKey("Addresses.AddressId"), nullable=True)
    TownshipId = Column(Integer, ForeignKey("Townships.TownshipId"), nullable=True)
    PropertyType = Column(String(50), nullable=True)
    CreatedDate = Column(DateTime, nullable=False, default=func.utcnow())
    ModifiedDate = Column(DateTime, nullable=False, default=func.utcnow())
    
    # Relationships
    address = relationship("Address", back_populates="properties")
    township = relationship("Township", back_populates="properties")
    surveys = relationship("Survey", back_populates="property")

class SurveyStatus(Base):
    __tablename__ = "SurveyStatuses"
    
    StatusId = Column(Integer, primary_key=True, index=True)
    StatusCode = Column(String(20), nullable=False, unique=True)
    StatusName = Column(String(100), nullable=False)
    SortOrder = Column(Integer, nullable=False, default=0)
    IsActive = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    surveys = relationship("Survey", back_populates="status")

class SurveyType(Base):
    __tablename__ = "SurveyTypes"
    
    SurveyTypeId = Column(Integer, primary_key=True, index=True)
    TypeName = Column(String(100), nullable=False, unique=True)
    TypeDescription = Column(String(500), nullable=True)
    EstimatedDuration = Column(Integer, nullable=True)
    BasePrice = Column(Numeric(10, 2), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    surveys = relationship("Survey", back_populates="survey_type")

class Survey(Base):
    __tablename__ = "Surveys"
    
    SurveyId = Column(Integer, primary_key=True, index=True)
    SurveyNumber = Column(String(50), nullable=False, index=True)
    CustomerId = Column(Integer, ForeignKey("Customers.CustomerId"), nullable=True)
    PropertyId = Column(Integer, ForeignKey("Properties.PropertyId"), nullable=True)
    SurveyTypeId = Column(Integer, ForeignKey("SurveyTypes.SurveyTypeId"), nullable=True)
    StatusId = Column(Integer, ForeignKey("SurveyStatuses.StatusId"), nullable=False)
    Title = Column(String(255), nullable=True)
    Description = Column(Text, nullable=True)
    PurposeCode = Column(String(50), nullable=True)
    RequestDate = Column(DateTime, nullable=True, default=func.utcnow())
    ScheduledDate = Column(DateTime, nullable=True)
    CompletedDate = Column(DateTime, nullable=True)
    DeliveryDate = Column(DateTime, nullable=True)
    DueDate = Column(DateTime, nullable=True, index=True)
    QuotedPrice = Column(Numeric(10, 2), nullable=True)
    FinalPrice = Column(Numeric(10, 2), nullable=True)
    IsFieldworkComplete = Column(Boolean, nullable=False, default=False)
    IsDrawingComplete = Column(Boolean, nullable=False, default=False)
    IsScanned = Column(Boolean, nullable=False, default=False)
    IsDelivered = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, default=func.utcnow())
    ModifiedDate = Column(DateTime, nullable=False, default=func.utcnow())
    CreatedBy = Column(String(100), nullable=True)
    ModifiedBy = Column(String(100), nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="surveys")
    property = relationship("Property", back_populates="surveys")
    survey_type = relationship("SurveyType", back_populates="surveys")
    status = relationship("SurveyStatus", back_populates="surveys")
    notes = relationship("SurveyNote", back_populates="survey")
    documents = relationship("SurveyDocument", back_populates="survey")

class SurveyNote(Base):
    __tablename__ = "SurveyNotes"
    
    NoteId = Column(Integer, primary_key=True, index=True)
    SurveyId = Column(Integer, ForeignKey("Surveys.SurveyId"), nullable=False)
    NoteType = Column(String(20), nullable=False)
    NoteText = Column(Text, nullable=False)
    IsInternal = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, default=func.utcnow())
    CreatedBy = Column(String(100), nullable=True)
    
    # Relationships
    survey = relationship("Survey", back_populates="notes")

class SurveyDocument(Base):
    __tablename__ = "SurveyDocuments"
    
    DocumentId = Column(Integer, primary_key=True, index=True)
    SurveyId = Column(Integer, ForeignKey("Surveys.SurveyId"), nullable=False)
    DocumentType = Column(String(50), nullable=False)
    FileName = Column(String(255), nullable=False)
    FilePath = Column(String(500), nullable=False)
    FileSize = Column(BigInteger, nullable=True)
    MimeType = Column(String(100), nullable=True)
    IsMainDocument = Column(Boolean, nullable=False, default=False)
    UploadedDate = Column(DateTime, nullable=False, default=func.utcnow())
    UploadedBy = Column(String(100), nullable=True)
    
    # Relationships
    survey = relationship("Survey", back_populates="documents")

class ZipCode(Base):
    __tablename__ = "ZIPCODES"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Add a primary key
    Zip = Column(Integer, nullable=True)
    Lat = Column(Float, nullable=True)
    Long = Column(Float, nullable=True)
    Town = Column(String(255), nullable=True)
    State = Column(String(255), nullable=True)
    County = Column(String(255), nullable=True)
    Type = Column(String(255), nullable=True)

class GeocodedID(Base):
    __tablename__ = "GeocodedIDs"
    
    ID = Column(String(50), primary_key=True)
