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
            # Keep Decimal as Decimal for DynamoDB - don't convert to float
            serialized[key] = value
        elif value is not None:  # Only skip None values
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
        elif isinstance(value, float) and key in ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']:
            # Convert float values back to Decimal for price fields
            deserialized[key] = Decimal(str(value))
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
        # First, get the total count of all items
        if search:
            filter_expression = Attr('CompanyName').contains(search) | \
                              Attr('CustomerCode').contains(search) | \
                              Attr('Email').contains(search)
            
            # Get total count with filter
            count_response = table.scan(
                FilterExpression=filter_expression,
                Select='COUNT'
            )
            total = count_response.get('Count', 0)
            
            # Get paginated items with filter
            response = table.scan(
                FilterExpression=filter_expression
            )
        else:
            # Get total count without filter
            count_response = table.scan(Select='COUNT')
            total = count_response.get('Count', 0)
            
            # Get all items without filter
            response = table.scan()
        
        items = response.get('Items', [])
        
        # Apply pagination to the results
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

def convert_survey_data(item_data: dict) -> dict:
    """Convert DynamoDB survey data to model format"""
    # Handle field name mapping - convert StatusId to SurveyStatusId for the model
    if 'StatusId' in item_data and 'SurveyStatusId' not in item_data:
        item_data['SurveyStatusId'] = item_data['StatusId']
        # Don't delete StatusId yet, we might need it for GraphQL responses
    
    # Convert Decimal objects to appropriate types
    for key, value in item_data.items():
        if isinstance(value, Decimal):
            # For price/cost fields, keep as Decimal for the model
            if key in ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']:
                # Keep as Decimal - no conversion needed
                pass
            else:
                # For ID fields that should be strings
                item_data[key] = str(value)
    
    # Convert string dates to datetime objects for datetime fields
    datetime_fields = ['CreatedDate', 'ModifiedDate', 'RequestDate', 'CompletedDate', 'ScheduledDate', 'DeliveryDate', 'DueDate']
    for field in datetime_fields:
        if field in item_data and isinstance(item_data[field], str):
            try:
                # Parse ISO format datetime strings
                item_data[field] = datetime.fromisoformat(item_data[field].replace('Z', '+00:00'))
            except ValueError:
                # If parsing fails, skip the field or use default
                if field in ['CreatedDate', 'ModifiedDate', 'RequestDate']:
                    item_data[field] = datetime.utcnow()
                else:
                    item_data[field] = None
    
    # Ensure required fields have default values if missing
    required_fields = {
        'CustomerId': str(uuid.uuid4()),
        'PropertyId': str(uuid.uuid4()),
        'SurveyTypeId': str(uuid.uuid4()),
        'SurveyStatusId': str(uuid.uuid4()),  # Use SurveyStatusId for the model
        'SurveyNumber': f"SURVEY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'CreatedDate': datetime.utcnow(),
        'ModifiedDate': datetime.utcnow(),
    }
    
    for field, default_value in required_fields.items():
        if field not in item_data or item_data[field] is None:
            item_data[field] = default_value
    
    return item_data

# Survey CRUD
def get_survey(survey_id: str) -> Optional[Survey]:
    """Get a single survey by ID"""
    table = get_table('Surveys')
    try:
        response = table.get_item(Key={'SurveyId': survey_id})
        item = response.get('Item')
        if item:
            item_data = deserialize_item(item)
            item_data = convert_survey_data(item_data)
            return Survey(**item_data)
        return None
    except ClientError as e:
        print(f"Error getting survey: {e}")
        return None
    except Exception as e:
        print(f"Error creating Survey model: {e}")
        print(f"Survey data: {item_data if 'item_data' in locals() else 'N/A'}")
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
        # First, get the total count of all items
        if search:
            filter_expression = Attr('SurveyNumber').contains(search) | \
                              Attr('Notes').contains(search)
            
            # Get total count with filter
            count_response = table.scan(
                FilterExpression=filter_expression,
                Select='COUNT'
            )
            total = count_response.get('Count', 0)
            
            # Get paginated items with filter
            response = table.scan(
                FilterExpression=filter_expression
            )
        else:
            # Get total count without filter
            count_response = table.scan(Select='COUNT')
            total = count_response.get('Count', 0)
            
            # Get all items without filter
            response = table.scan()
        
        items = response.get('Items', [])
        
        # Apply pagination to the results
        paginated_items = items[skip:skip + limit]
        
        surveys = []
        for item in paginated_items:
            try:
                # Deserialize and convert data
                item_data = deserialize_item(item)
                item_data = convert_survey_data(item_data)
                
                survey = Survey(**item_data)
                surveys.append(survey)
            except Exception as e:
                print(f"Error creating survey from item {item}: {e}")
                continue
                
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
    
    # Convert float values to Decimal for DynamoDB compatibility
    decimal_fields = ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']
    for field in decimal_fields:
        if field in survey_data and isinstance(survey_data[field], (int, float)):
            survey_data[field] = Decimal(str(survey_data[field]))
    
    try:
        serialized_data = serialize_item(survey_data)
        table.put_item(Item=serialized_data)
        return Survey(**survey_data)
    except ClientError as e:
        print(f"Error creating survey: {e}")
        return None

def update_survey(survey_id: str, survey: schemas.SurveyUpdate) -> Optional[Survey]:
    """Update an existing survey"""
    table = get_table('Surveys')
    
    # First check if survey exists
    existing_survey = get_survey(survey_id)
    if not existing_survey:
        return None
    
    # Get only the fields that were provided (non-None values)
    survey_data = survey.dict(exclude_unset=True)
    survey_data['ModifiedDate'] = datetime.utcnow()
    
    # Handle field name mapping - convert StatusId to SurveyStatusId for DynamoDB
    if 'StatusId' in survey_data:
        survey_data['SurveyStatusId'] = survey_data.pop('StatusId')
    
    # Convert float values to Decimal for DynamoDB compatibility
    decimal_fields = ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']
    for field in decimal_fields:
        if field in survey_data and isinstance(survey_data[field], (int, float)):
            survey_data[field] = Decimal(str(survey_data[field]))
    
    # Build update expression
    update_expression = "SET "
    expression_attribute_names = {}
    expression_attribute_values = {}
    
    for key, value in survey_data.items():
        if key != 'SurveyId':  # Don't update the primary key
            update_expression += f"#{key} = :{key}, "
            expression_attribute_names[f"#{key}"] = key
            expression_attribute_values[f":{key}"] = value
    
    # Remove trailing comma and space
    update_expression = update_expression.rstrip(", ")
    
    try:
        serialized_values = serialize_item(expression_attribute_values)
        response = table.update_item(
            Key={'SurveyId': survey_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=serialized_values,
            ReturnValues="ALL_NEW"
        )
        
        if response.get('Attributes'):
            updated_data = deserialize_item(response['Attributes'])
            print(f"After deserialize_item: {[(k, type(v), v) for k, v in updated_data.items() if k in ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']]}")
            updated_data = convert_survey_data(updated_data)
            print(f"After convert_survey_data: {[(k, type(v), v) for k, v in updated_data.items() if k in ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']]}")
            print(f"All data types before Survey creation: {[(k, type(v)) for k, v in updated_data.items()]}")
            return Survey(**updated_data)
        return None
    except ClientError as e:
        print(f"Error updating survey: {e}")
        return None
    except Exception as e:
        print(f"Error creating updated Survey model: {e}")
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
                PropertyId=1,  # Use integer ID to match frontend
                PropertyCode="PROP001",
                PropertyName="Mock Property 1",
                PropertyDescription="A sample property for testing",
                OwnerName="John Owner",
                OwnerPhone="555-0001",
                OwnerEmail="john@mockowner1.com",
                AddressId=101,  # Add numeric AddressId
                TownshipId=201,  # Add numeric TownshipId
                SurveyPrimaryKey=301,  # Add numeric SurveyPrimaryKey
                LegacyTax="TAX001",
                District="District 1",
                Section="Section A",
                Block="Block 1",
                Lot="Lot 1",
                PropertyType="Residential",
                IsActive=True
            ),
            Property(
                PropertyId=2,  # Use integer ID to match frontend
                PropertyCode="PROP002",
                PropertyName="Mock Property 2", 
                PropertyDescription="Another sample property for testing",
                OwnerName="Jane Owner",
                OwnerPhone="555-0002", 
                OwnerEmail="jane@mockowner2.com",
                AddressId=102,  # Add numeric AddressId
                TownshipId=202,  # Add numeric TownshipId
                SurveyPrimaryKey=302,  # Add numeric SurveyPrimaryKey
                LegacyTax="TAX002",
                District="District 2",
                Section="Section B",
                Block="Block 2",
                Lot="Lot 2",
                PropertyType="Commercial",
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
        # First, get the total count of all items
        if search:
            filter_expression = Attr('PropertyName').contains(search) | \
                              Attr('PropertyCode').contains(search) | \
                              Attr('OwnerName').contains(search)
            
            # Get total count with filter
            count_response = table.scan(
                FilterExpression=filter_expression,
                Select='COUNT'
            )
            total = count_response.get('Count', 0)
            
            # Get paginated items with filter
            response = table.scan(
                FilterExpression=filter_expression
            )
        else:
            # Get total count without filter
            count_response = table.scan(Select='COUNT')
            total = count_response.get('Count', 0)
            
            # Get all items without filter
            response = table.scan()
        
        items = response.get('Items', [])
        
        # Apply pagination to the results
        paginated_items = items[skip:skip + limit]
        
        properties = [Property(**deserialize_item(item)) for item in paginated_items]
        return properties, total
        
    except ClientError as e:
        print(f"Error getting properties: {e}")
        return [], 0

def create_property(property: schemas.PropertyCreate) -> Optional[Property]:
    """Create a new property"""
    table = get_table('Properties')
    
    # Include all fields, even those with None values
    property_data = property.dict(exclude_unset=False)
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

def update_property(property_id: str, property: schemas.PropertyUpdate) -> Optional[Property]:
    """Update an existing property"""
    table = get_table('Properties')
    
    try:
        # Get existing property first
        response = table.get_item(Key={'PropertyId': property_id})
        if 'Item' not in response:
            print(f"Property {property_id} not found")
            return None
        
        existing_property = deserialize_item(response['Item'])
        
        # Update with new data
        property_data = property.dict(exclude_unset=True)
        existing_property.update(property_data)
        existing_property['ModifiedDate'] = datetime.utcnow()
        
        # Save updated property
        serialized_data = serialize_item(existing_property)
        table.put_item(Item=serialized_data)
        return Property(**existing_property)
        
    except ClientError as e:
        print(f"Error updating property: {e}")
        return None

def delete_property(property_id: str) -> bool:
    """Delete a property"""
    table = get_table('Properties')
    
    try:
        response = table.delete_item(
            Key={'PropertyId': property_id},
            ReturnValues='ALL_OLD'
        )
        # Check if the item existed before deletion
        return 'Attributes' in response
    except ClientError as e:
        print(f"Error deleting property: {e}")
        return False

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

def create_survey_type(survey_type: SurveyType) -> Optional[SurveyType]:
    """Create a new survey type"""
    table = get_table('SurveyTypes')
    
    try:
        item_data = survey_type.dict()
        serialized_data = serialize_item(item_data)
        
        table.put_item(Item=serialized_data)
        return survey_type
    except ClientError as e:
        print(f"Error creating survey type: {e}")
        return None

def create_survey_status(survey_status: SurveyStatus) -> Optional[SurveyStatus]:
    """Create a new survey status"""
    table = get_table('SurveyStatuses')
    
    try:
        item_data = survey_status.dict()
        serialized_data = serialize_item(item_data)
        
        table.put_item(Item=serialized_data)
        return survey_status
    except ClientError as e:
        print(f"Error creating survey status: {e}")
        return None


def update_survey_status(survey_status_id: str, survey_status_update: schemas.SurveyStatusUpdate) -> Optional[SurveyStatus]:
    """Update an existing survey status"""
    table = get_table('SurveyStatuses')
    try:
        # First, get the existing survey status
        response = table.get_item(Key={'SurveyStatusId': survey_status_id})
        if 'Item' not in response:
            return None
        
        # Update the fields
        update_data = survey_status_update.dict(exclude_unset=True)
        
        # Build update expression
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        for key, value in update_data.items():
            if key != 'SurveyStatusId':  # Don't update the ID
                # Handle reserved keywords
                attr_name = f"#{key}"
                attr_value = f":{key}"
                expression_attribute_names[attr_name] = key
                expression_attribute_values[attr_value] = value
                update_expression += f"{attr_name} = {attr_value}, "
        
        # Remove trailing comma and space
        update_expression = update_expression.rstrip(", ")
        
        # Add UpdatedDate
        expression_attribute_names["#UpdatedDate"] = "UpdatedDate"
        expression_attribute_values[":UpdatedDate"] = datetime.now().isoformat()
        update_expression += ", #UpdatedDate = :UpdatedDate"
        
        # Update the item
        response = table.update_item(
            Key={'SurveyStatusId': survey_status_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        
        updated_item = response.get('Attributes')
        if updated_item:
            return SurveyStatus(**deserialize_item(updated_item))
        return None
        
    except ClientError as e:
        print(f"Error updating survey status {survey_status_id}: {e}")
        return None


# Township CRUD
def get_township(township_id: str) -> Optional[Township]:
    """Get a single township by ID"""
    table = get_table('Townships')
    try:
        response = table.get_item(Key={'TownshipId': township_id})
        item = response.get('Item')
        if item:
            return Township(**deserialize_item(item))
        return None
    except ClientError as e:
        print(f"Error getting township {township_id}: {e}")
        return None


def get_townships(skip: int = 0, limit: int = 100, search: Optional[str] = None) -> tuple[List[Township], int]:
    """Get townships with pagination and optional search"""
    table = get_table('Townships')
    try:
        filter_expression = Attr('IsActive').eq(True)
        
        if search:
            search_filter = (
                Attr('TownshipName').contains(search) |
                Attr('County').contains(search) |
                Attr('State').contains(search)
            )
            filter_expression = filter_expression & search_filter
        
        response = table.scan(FilterExpression=filter_expression)
        items = response.get('Items', [])
        
        # Convert to Township objects
        townships = [Township(**deserialize_item(item)) for item in items]
        
        # Sort by TownshipName
        townships.sort(key=lambda x: x.TownshipName.lower())
        
        # Apply pagination
        total = len(townships)
        start = skip
        end = skip + limit
        paginated_townships = townships[start:end]
        
        return paginated_townships, total
        
    except ClientError as e:
        print(f"Error getting townships: {e}")
        return [], 0


def create_township(township: schemas.TownshipCreate) -> Optional[Township]:
    """Create a new township"""
    table = get_table('Townships')
    try:
        # Create Township object
        new_township = Township(
            TownshipName=township.TownshipName,
            County=township.County,
            State=township.State,
            IsActive=township.IsActive,
            CreatedBy="system",  # TODO: get from auth context
            ModifiedBy="system"
        )
        
        # Serialize for DynamoDB
        item = serialize_item(new_township.model_dump())
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        return new_township
        
    except ClientError as e:
        print(f"Error creating township: {e}")
        return None


def update_township(township_id: str, township: schemas.TownshipUpdate) -> Optional[Township]:
    """Update an existing township"""
    table = get_table('Townships')
    try:
        # Get existing township
        existing = get_township(township_id)
        if not existing:
            return None
        
        # Update fields
        update_expression = "SET ModifiedDate = :modified_date, ModifiedBy = :modified_by"
        expression_values = {
            ':modified_date': serialize_datetime(datetime.utcnow()),
            ':modified_by': "system"  # TODO: get from auth context
        }
        
        if township.TownshipName is not None:
            update_expression += ", TownshipName = :township_name"
            expression_values[':township_name'] = township.TownshipName
        
        if township.County is not None:
            update_expression += ", County = :county"
            expression_values[':county'] = township.County
        
        if township.State is not None:
            update_expression += ", #state = :state"
            expression_values[':state'] = township.State
        
        if township.IsActive is not None:
            update_expression += ", IsActive = :is_active"
            expression_values[':is_active'] = township.IsActive
        
        # Update in DynamoDB
        response = table.update_item(
            Key={'TownshipId': township_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames={'#state': 'State'} if township.State is not None else {},
            ReturnValues='ALL_NEW'
        )
        
        # Return updated township
        item = response.get('Attributes')
        if item:
            return Township(**deserialize_item(item))
        return None
        
    except ClientError as e:
        print(f"Error updating township {township_id}: {e}")
        return None


def delete_township(township_id: str) -> bool:
    """Soft delete a township by setting IsActive to False"""
    table = get_table('Townships')
    try:
        # Update IsActive to False instead of actually deleting
        table.update_item(
            Key={'TownshipId': township_id},
            UpdateExpression='SET IsActive = :is_active, ModifiedDate = :modified_date, ModifiedBy = :modified_by',
            ExpressionAttributeValues={
                ':is_active': False,
                ':modified_date': serialize_datetime(datetime.utcnow()),
                ':modified_by': "system"  # TODO: get from auth context
            }
        )
        return True
        
    except ClientError as e:
        print(f"Error deleting township {township_id}: {e}")
        return False