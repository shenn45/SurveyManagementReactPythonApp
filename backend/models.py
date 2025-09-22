from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
import uuid

# DynamoDB models using Pydantic BaseModel

class Address(BaseModel):
    AddressId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    AddressType: str
    AddressLine1: str
    AddressLine2: Optional[str] = None
    City: str
    StateCode: str
    ZipCode: str
    County: Optional[str] = None
    Country: str = "USA"
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Customer(BaseModel):
    CustomerId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    CustomerCode: str
    CompanyName: str
    ContactFirstName: Optional[str] = None
    ContactLastName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Website: Optional[str] = None
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    # For DynamoDB relationships, we'll use lists of IDs
    AddressIds: List[str] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CustomerAddress(BaseModel):
    CustomerAddressId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    CustomerId: str
    AddressId: str
    IsPrimary: bool = False
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Township(BaseModel):
    TownshipId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    TownshipName: str
    County: str
    State: str
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Property(BaseModel):
    PropertyId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    PropertyCode: str
    PropertyName: str
    PropertyDescription: Optional[str] = None
    OwnerName: Optional[str] = None
    OwnerPhone: Optional[str] = None
    OwnerEmail: Optional[str] = None
    AddressId: Optional[str] = None
    TownshipId: Optional[str] = None
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SurveyType(BaseModel):
    SurveyTypeId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    SurveyTypeName: str
    Description: Optional[str] = None
    IsActive: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SurveyStatus(BaseModel):
    SurveyStatusId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    StatusName: str
    Description: Optional[str] = None
    IsActive: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Survey(BaseModel):
    SurveyId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    SurveyNumber: str
    SurveyTypeId: str
    CustomerId: str
    PropertyId: str
    SurveyStatusId: str
    EstimatedCost: Optional[Decimal] = None
    ActualCost: Optional[Decimal] = None
    RequestDate: datetime = Field(default_factory=datetime.utcnow)
    CompletedDate: Optional[datetime] = None
    Notes: Optional[str] = None
    SurveyorNotes: Optional[str] = None
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    ModifiedDate: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[str] = None
    ModifiedBy: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class SurveyFile(BaseModel):
    SurveyFileId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    SurveyId: str
    FileName: str
    FileType: str
    FileSize: int
    FilePath: str
    Description: Optional[str] = None
    IsActive: bool = True
    CreatedDate: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Document(BaseModel):
    DocumentId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    DocumentName: str
    DocumentType: str
    DocumentSize: int
    DocumentPath: str
    Description: Optional[str] = None
    UploadedBy: Optional[str] = None
    UploadedDate: datetime = Field(default_factory=datetime.utcnow)
    IsActive: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# DynamoDB table configurations
DYNAMODB_TABLES = {
    'Addresses': {
        'TableName': 'Addresses',
        'KeySchema': [
            {'AttributeName': 'AddressId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'AddressId', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'AddressTypeIndex',
                'KeySchema': [
                    {'AttributeName': 'AddressType', 'KeyType': 'HASH'}
                ],
                'AttributeDefinitions': [
                    {'AttributeName': 'AddressType', 'AttributeType': 'S'}
                ]
            }
        ]
    },
    'Customers': {
        'TableName': 'Customers',
        'KeySchema': [
            {'AttributeName': 'CustomerId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'CustomerId', 'AttributeType': 'S'},
            {'AttributeName': 'CustomerCode', 'AttributeType': 'S'},
            {'AttributeName': 'CompanyName', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'CustomerCodeIndex',
                'KeySchema': [
                    {'AttributeName': 'CustomerCode', 'KeyType': 'HASH'}
                ]
            },
            {
                'IndexName': 'CompanyNameIndex',
                'KeySchema': [
                    {'AttributeName': 'CompanyName', 'KeyType': 'HASH'}
                ]
            }
        ]
    },
    'CustomerAddresses': {
        'TableName': 'CustomerAddresses',
        'KeySchema': [
            {'AttributeName': 'CustomerAddressId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'CustomerAddressId', 'AttributeType': 'S'},
            {'AttributeName': 'CustomerId', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'CustomerIdIndex',
                'KeySchema': [
                    {'AttributeName': 'CustomerId', 'KeyType': 'HASH'}
                ]
            }
        ]
    },
    'Townships': {
        'TableName': 'Townships',
        'KeySchema': [
            {'AttributeName': 'TownshipId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'TownshipId', 'AttributeType': 'S'},
            {'AttributeName': 'TownshipName', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'TownshipNameIndex',
                'KeySchema': [
                    {'AttributeName': 'TownshipName', 'KeyType': 'HASH'}
                ]
            }
        ]
    },
    'Properties': {
        'TableName': 'Properties',
        'KeySchema': [
            {'AttributeName': 'PropertyId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'PropertyId', 'AttributeType': 'S'},
            {'AttributeName': 'PropertyCode', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'PropertyCodeIndex',
                'KeySchema': [
                    {'AttributeName': 'PropertyCode', 'KeyType': 'HASH'}
                ]
            }
        ]
    },
    'SurveyTypes': {
        'TableName': 'SurveyTypes',
        'KeySchema': [
            {'AttributeName': 'SurveyTypeId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'SurveyTypeId', 'AttributeType': 'S'}
        ]
    },
    'SurveyStatuses': {
        'TableName': 'SurveyStatuses',
        'KeySchema': [
            {'AttributeName': 'SurveyStatusId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'SurveyStatusId', 'AttributeType': 'S'}
        ]
    },
    'Surveys': {
        'TableName': 'Surveys',
        'KeySchema': [
            {'AttributeName': 'SurveyId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'SurveyId', 'AttributeType': 'S'},
            {'AttributeName': 'SurveyNumber', 'AttributeType': 'S'},
            {'AttributeName': 'CustomerId', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'SurveyNumberIndex',
                'KeySchema': [
                    {'AttributeName': 'SurveyNumber', 'KeyType': 'HASH'}
                ]
            },
            {
                'IndexName': 'CustomerIdIndex',
                'KeySchema': [
                    {'AttributeName': 'CustomerId', 'KeyType': 'HASH'}
                ]
            }
        ]
    },
    'SurveyFiles': {
        'TableName': 'SurveyFiles',
        'KeySchema': [
            {'AttributeName': 'SurveyFileId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'SurveyFileId', 'AttributeType': 'S'},
            {'AttributeName': 'SurveyId', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'SurveyIdIndex',
                'KeySchema': [
                    {'AttributeName': 'SurveyId', 'KeyType': 'HASH'}
                ]
            }
        ]
    },
    'Documents': {
        'TableName': 'Documents',
        'KeySchema': [
            {'AttributeName': 'DocumentId', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'DocumentId', 'AttributeType': 'S'}
        ]
    }
}
