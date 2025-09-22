from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
import uuid

from database import get_table
from models import *
import schemas

# Helper functions
def serialize_datetime(obj):
    """Convert datetime objects to ISO string format for DynamoDB"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def serialize_item(item: dict) -> dict:
    """Serialize Python objects for DynamoDB storage"""
    serialized = {}
    for key, value in item.items():
        if isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, Decimal):
            serialized[key] = float(value)
        else:
            serialized[key] = value
    return serialized

def deserialize_item(item: dict) -> dict:
    """Deserialize DynamoDB item to Python objects"""
    if not item:
        return None
    
    deserialized = {}
    for key, value in item.items():
        if key.endswith('Date') and isinstance(value, str):
            try:
                deserialized[key] = datetime.fromisoformat(value)
            except ValueError:
                deserialized[key] = value
        else:
            deserialized[key] = value
    return deserialized

# Customer CRUD
def get_customer(customer_id: str) -> Optional[Customer]:
    """Get a single customer by ID"""
    table = get_table('Customers')
    try:
        response = table.get_item(Key={'CustomerId': customer_id})
        item = response.get('Item')
        if item:
            return Customer(**deserialize_item(item))
        return None
    except ClientError as e:
        print(f"Error getting customer: {e}")
        return None

def get_customers(skip: int = 0, limit: int = 100, search: Optional[str] = None) -> tuple[List[Customer], int]:
    """Get customers with pagination and optional search"""
    table = get_table('Customers')
    
    # Handle when DynamoDB is not available
    if table is None:
        print("Using mock customer data")
        mock_customers = [
            Customer(
                CustomerId="mock-customer-1",
                CustomerCode="MOCK001",
                CompanyName="Mock Company 1",
                ContactFirstName="John",
                ContactLastName="Doe",
                Email="john@mockcompany1.com",
                Phone="555-0001",
                IsActive=True
            ),
            Customer(
                CustomerId="mock-customer-2", 
                CustomerCode="MOCK002",
                CompanyName="Mock Company 2",
                ContactFirstName="Jane",
                ContactLastName="Smith",
                Email="jane@mockcompany2.com",
                Phone="555-0002",
                IsActive=True
            )
        ]
        
        # Apply search filter if provided
        if search:
            filtered_customers = [
                c for c in mock_customers 
                if search.lower() in c.CompanyName.lower() or 
                   search.lower() in c.CustomerCode.lower() or
                   search.lower() in c.Email.lower()
            ]
        else:
            filtered_customers = mock_customers
            
        total = len(filtered_customers)
        paginated_customers = filtered_customers[skip:skip + limit]
        return paginated_customers, total
    
    try:
        if search:
            filter_expression = Attr('CompanyName').contains(search) | \
                              Attr('CustomerCode').contains(search) | \
                              Attr('Email').contains(search)
            
            response = table.scan(
                FilterExpression=filter_expression,
                Limit=limit + skip
            )
        else:
            response = table.scan(Limit=limit + skip)
        
        items = response.get('Items', [])
        total = len(items)
        paginated_items = items[skip:skip + limit]
        
        customers = [Customer(**deserialize_item(item)) for item in paginated_items]
        return customers, total
        
    except ClientError as e:
        print(f"Error getting customers: {e}")
        return [], 0

def create_customer(customer: schemas.CustomerCreate) -> Optional[Customer]:
    """Create a new customer"""
    table = get_table('Customers')
    
    customer_data = customer.dict()
    customer_data['CustomerId'] = str(uuid.uuid4())
    customer_data['CreatedDate'] = datetime.utcnow()
    customer_data['ModifiedDate'] = datetime.utcnow()
    
    # Handle when DynamoDB is not available
    if table is None:
        print(f"Mock: Creating customer {customer_data['CompanyName']}")
        return Customer(**customer_data)
    
    try:
        serialized_data = serialize_item(customer_data)
        table.put_item(Item=serialized_data)
        return Customer(**customer_data)
    except ClientError as e:
        print(f"Error creating customer: {e}")
        return None

def update_customer(customer_id: str, customer: schemas.CustomerUpdate) -> Optional[Customer]:
    """Update an existing customer"""
    table = get_table('Customers')
    
    update_data = customer.dict(exclude_unset=True)
    update_data['ModifiedDate'] = datetime.utcnow()
    
    update_expression_parts = []
    expression_attribute_values = {}
    
    for key, value in update_data.items():
        update_expression_parts.append(f"{key} = :{key}")
        expression_attribute_values[f":{key}"] = serialize_datetime(value)
    
    update_expression = "SET " + ", ".join(update_expression_parts)
    
    try:
        response = table.update_item(
            Key={'CustomerId': customer_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        
        updated_item = response.get('Attributes')
        if updated_item:
            return Customer(**deserialize_item(updated_item))
        return None
        
    except ClientError as e:
        print(f"Error updating customer: {e}")
        return None

def delete_customer(customer_id: str) -> bool:
    """Delete a customer (soft delete by setting IsActive to False)"""
    table = get_table('Customers')
    
    try:
        table.update_item(
            Key={'CustomerId': customer_id},
            UpdateExpression="SET IsActive = :inactive, ModifiedDate = :modified",
            ExpressionAttributeValues={
                ':inactive': False,
                ':modified': datetime.utcnow().isoformat()
            }
        )
        return True
    except ClientError as e:
        print(f"Error deleting customer: {e}")
        return False

# Survey CRUD
def get_survey(survey_id: str) -> Optional[Survey]:
    """Get a single survey by ID"""
    table = get_table('Surveys')
    try:
        response = table.get_item(Key={'SurveyId': survey_id})
        item = response.get('Item')
        if item:
            return Survey(**deserialize_item(item))
        return None
    except ClientError as e:
        print(f"Error getting survey: {e}")
        return None

def get_surveys(skip: int = 0, limit: int = 100, search: Optional[str] = None) -> tuple[List[Survey], int]:
    """Get surveys with pagination and optional search"""
    table = get_table('Surveys')
    
    # Handle when DynamoDB is not available
    if table is None:
        print("Using mock survey data")
        mock_surveys = [
            Survey(
                SurveyId="mock-survey-1",
                SurveyNumber="SURV001",
                CustomerId="mock-customer-1",
                PropertyId="mock-property-1",
                SurveyDate=datetime.utcnow().date(),
                Notes="Mock survey for testing"
            ),
            Survey(
                SurveyId="mock-survey-2",
                SurveyNumber="SURV002", 
                CustomerId="mock-customer-2",
                PropertyId="mock-property-2",
                SurveyDate=datetime.utcnow().date(),
                Notes="Another mock survey"
            )
        ]
        
        # Apply search filter if provided
        if search:
            filtered_surveys = [
                s for s in mock_surveys 
                if search.lower() in s.SurveyNumber.lower() or 
                   search.lower() in s.Notes.lower()
            ]
        else:
            filtered_surveys = mock_surveys
            
        total = len(filtered_surveys)
        paginated_surveys = filtered_surveys[skip:skip + limit]
        return paginated_surveys, total
    
    try:
        if search:
            filter_expression = Attr('SurveyNumber').contains(search) | \
                              Attr('Notes').contains(search)
            
            response = table.scan(
                FilterExpression=filter_expression,
                Limit=limit + skip
            )
        else:
            response = table.scan(Limit=limit + skip)
        
        items = response.get('Items', [])
        total = len(items)
        paginated_items = items[skip:skip + limit]
        
        surveys = [Survey(**deserialize_item(item)) for item in paginated_items]
        return surveys, total
        
    except ClientError as e:
        print(f"Error getting surveys: {e}")
        return [], 0

def create_survey(survey: schemas.SurveyCreate) -> Optional[Survey]:
    """Create a new survey"""
    table = get_table('Surveys')
    
    survey_data = survey.dict()
    survey_data['SurveyId'] = str(uuid.uuid4())
    survey_data['CreatedDate'] = datetime.utcnow()
    survey_data['ModifiedDate'] = datetime.utcnow()
    survey_data['RequestDate'] = datetime.utcnow()
    
    try:
        serialized_data = serialize_item(survey_data)
        table.put_item(Item=serialized_data)
        return Survey(**survey_data)
    except ClientError as e:
        print(f"Error creating survey: {e}")
        return None

# Property CRUD
def get_property(property_id: str) -> Optional[Property]:
    """Get a single property by ID"""
    table = get_table('Properties')
    try:
        response = table.get_item(Key={'PropertyId': property_id})
        item = response.get('Item')
        if item:
            return Property(**deserialize_item(item))
        return None
    except ClientError as e:
        print(f"Error getting property: {e}")
        return None

def get_properties(skip: int = 0, limit: int = 100, search: Optional[str] = None) -> tuple[List[Property], int]:
    """Get properties with pagination and optional search"""
    table = get_table('Properties')
    
    # Handle when DynamoDB is not available
    if table is None:
        print("Using mock property data")
        mock_properties = [
            Property(
                PropertyId="mock-property-1",
                PropertyCode="PROP001",
                PropertyName="Mock Property 1",
                Address="123 Main St",
                City="Springfield",
                State="IL",
                PostalCode="62701",
                OwnerName="John Owner",
                IsActive=True
            ),
            Property(
                PropertyId="mock-property-2",
                PropertyCode="PROP002",
                PropertyName="Mock Property 2", 
                Address="456 Oak Ave",
                City="Springfield",
                State="IL",
                PostalCode="62702",
                OwnerName="Jane Owner",
                IsActive=True
            )
        ]
        
        # Apply search filter if provided
        if search:
            filtered_properties = [
                p for p in mock_properties 
                if search.lower() in p.PropertyName.lower() or 
                   search.lower() in p.PropertyCode.lower() or
                   search.lower() in p.OwnerName.lower()
            ]
        else:
            filtered_properties = mock_properties
            
        total = len(filtered_properties)
        paginated_properties = filtered_properties[skip:skip + limit]
        return paginated_properties, total
    
    try:
        if search:
            filter_expression = Attr('PropertyName').contains(search) | \
                              Attr('PropertyCode').contains(search) | \
                              Attr('OwnerName').contains(search)
            
            response = table.scan(
                FilterExpression=filter_expression,
                Limit=limit + skip
            )
        else:
            response = table.scan(Limit=limit + skip)
        
        items = response.get('Items', [])
        total = len(items)
        paginated_items = items[skip:skip + limit]
        
        properties = [Property(**deserialize_item(item)) for item in paginated_items]
        return properties, total
        
    except ClientError as e:
        print(f"Error getting properties: {e}")
        return [], 0

def create_property(property: schemas.PropertyCreate) -> Optional[Property]:
    """Create a new property"""
    table = get_table('Properties')
    
    property_data = property.dict()
    property_data['PropertyId'] = str(uuid.uuid4())
    property_data['CreatedDate'] = datetime.utcnow()
    property_data['ModifiedDate'] = datetime.utcnow()
    
    try:
        serialized_data = serialize_item(property_data)
        table.put_item(Item=serialized_data)
        return Property(**property_data)
    except ClientError as e:
        print(f"Error creating property: {e}")
        return None

# Survey Type CRUD
def get_survey_types() -> List[SurveyType]:
    """Get all active survey types"""
    table = get_table('SurveyTypes')
    try:
        response = table.scan(
            FilterExpression=Attr('IsActive').eq(True)
        )
        items = response.get('Items', [])
        return [SurveyType(**deserialize_item(item)) for item in items]
    except ClientError as e:
        print(f"Error getting survey types: {e}")
        return []

# Survey Status CRUD
def get_survey_statuses() -> List[SurveyStatus]:
    """Get all active survey statuses"""
    table = get_table('SurveyStatuses')
    try:
        response = table.scan(
            FilterExpression=Attr('IsActive').eq(True)
        )
        items = response.get('Items', [])
        return [SurveyStatus(**deserialize_item(item)) for item in items]
    except ClientError as e:
        print(f"Error getting survey statuses: {e}")
        return []