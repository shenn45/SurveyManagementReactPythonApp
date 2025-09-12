from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, BigInteger, Float, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
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
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    
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
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    ModifiedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
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
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="customer_addresses")
    address = relationship("Address", back_populates="customer_addresses")

class Township(Base):
    __tablename__ = "Townships"
    
    TownshipId = Column(Integer, primary_key=True, index=True)
    TownshipName = Column(String(100), nullable=False, unique=True)
    County = Column(String(100), nullable=False)
    State = Column(String(50), nullable=False)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    ModifiedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    CreatedBy = Column(String(100), nullable=True)
    ModifiedBy = Column(String(100), nullable=True)
    
    # Relationships
    properties = relationship("Property", back_populates="township")

class Property(Base):
    __tablename__ = "Properties"
    
    PropertyId = Column(Integer, primary_key=True, index=True)
    PropertyCode = Column(String(50), nullable=False, unique=True)
    PropertyName = Column(String(255), nullable=False, index=True)
    PropertyDescription = Column(Text, nullable=True)
    OwnerName = Column(String(255), nullable=True)
    OwnerPhone = Column(String(20), nullable=True)
    OwnerEmail = Column(String(255), nullable=True)
    AddressId = Column(Integer, ForeignKey("Addresses.AddressId"), nullable=True)
    TownshipId = Column(Integer, ForeignKey("Townships.TownshipId"), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    ModifiedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    CreatedBy = Column(String(100), nullable=True)
    ModifiedBy = Column(String(100), nullable=True)
    
    # Relationships
    address = relationship("Address", back_populates="properties")
    township = relationship("Township", back_populates="properties")
    surveys = relationship("Survey", back_populates="property")

class SurveyType(Base):
    __tablename__ = "SurveyTypes"
    
    SurveyTypeId = Column(Integer, primary_key=True, index=True)
    SurveyTypeName = Column(String(100), nullable=False, unique=True)
    Description = Column(Text, nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    surveys = relationship("Survey", back_populates="survey_type")

class SurveyStatus(Base):
    __tablename__ = "SurveyStatuses"
    
    SurveyStatusId = Column(Integer, primary_key=True, index=True)
    StatusName = Column(String(50), nullable=False, unique=True)
    Description = Column(Text, nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    surveys = relationship("Survey", back_populates="survey_status")

class Survey(Base):
    __tablename__ = "Surveys"
    
    SurveyId = Column(Integer, primary_key=True, index=True)
    SurveyNumber = Column(String(50), nullable=False, unique=True)
    SurveyTypeId = Column(Integer, ForeignKey("SurveyTypes.SurveyTypeId"), nullable=False)
    CustomerId = Column(Integer, ForeignKey("Customers.CustomerId"), nullable=False)
    PropertyId = Column(Integer, ForeignKey("Properties.PropertyId"), nullable=False)
    SurveyStatusId = Column(Integer, ForeignKey("SurveyStatuses.SurveyStatusId"), nullable=False)
    EstimatedCost = Column(Numeric(10, 2), nullable=True)
    ActualCost = Column(Numeric(10, 2), nullable=True)
    RequestDate = Column(DateTime, nullable=True, default=datetime.utcnow)
    CompletedDate = Column(DateTime, nullable=True)
    Notes = Column(Text, nullable=True)
    SurveyorNotes = Column(Text, nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    ModifiedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    CreatedBy = Column(String(100), nullable=True)
    ModifiedBy = Column(String(100), nullable=True)
    
    # Relationships
    survey_type = relationship("SurveyType", back_populates="surveys")
    customer = relationship("Customer", back_populates="surveys")
    property = relationship("Property", back_populates="surveys")
    survey_status = relationship("SurveyStatus", back_populates="surveys")
    survey_files = relationship("SurveyFile", back_populates="survey")

class SurveyFile(Base):
    __tablename__ = "SurveyFiles"
    
    SurveyFileId = Column(Integer, primary_key=True, index=True)
    SurveyId = Column(Integer, ForeignKey("Surveys.SurveyId"), nullable=False)
    FileName = Column(String(255), nullable=False)
    FileType = Column(String(50), nullable=False)
    FileSize = Column(BigInteger, nullable=False)
    FilePath = Column(String(500), nullable=False)
    Description = Column(Text, nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    survey = relationship("Survey", back_populates="survey_files")

class Document(Base):
    __tablename__ = "Documents"
    
    DocumentId = Column(Integer, primary_key=True, index=True)
    DocumentName = Column(String(255), nullable=False)
    DocumentType = Column(String(50), nullable=False)
    DocumentSize = Column(BigInteger, nullable=False)
    DocumentPath = Column(String(500), nullable=False)
    Description = Column(Text, nullable=True)
    UploadedBy = Column(String(100), nullable=True)
    UploadedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    IsActive = Column(Boolean, nullable=False, default=True)
