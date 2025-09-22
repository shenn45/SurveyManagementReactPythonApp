"""
Pytest configuration and fixtures for Survey Management App tests
"""
import os
import pytest
import boto3
from moto import mock_aws
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime, timezone
import uuid

# Import our application modules
from fastapi import FastAPI
# from main import app  # Temporarily disabled for testing
from models import Customer, Survey, Property, DYNAMODB_TABLES
from database import get_dynamodb

# Create a test FastAPI app
test_app = FastAPI(title="Test Survey Management API")


@pytest.fixture(scope="session")
def test_env_vars():
    """Set up test environment variables"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["DYNAMODB_ENDPOINT_URL"] = ""  # Use moto mock
    

@pytest.fixture
def mock_dynamodb_tables(test_env_vars):
    """Create mock DynamoDB tables for testing"""
    with mock_aws():
        # Create DynamoDB resource
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create each table from our configuration
        for table_name, table_config in DYNAMODB_TABLES.items():
            create_params = {
                'TableName': table_config['TableName'],
                'KeySchema': table_config['KeySchema'],
                'AttributeDefinitions': table_config['AttributeDefinitions'],
                'BillingMode': 'PAY_PER_REQUEST'
            }
            
            # Add Global Secondary Indexes if they exist
            if 'GlobalSecondaryIndexes' in table_config:
                gsi_config = []
                for gsi in table_config['GlobalSecondaryIndexes']:
                    gsi_item = {
                        'IndexName': gsi['IndexName'],
                        'KeySchema': gsi['KeySchema'],
                        'Projection': {'ProjectionType': 'ALL'}
                    }
                    gsi_config.append(gsi_item)
                    
                    # Add any missing attribute definitions for GSI
                    for attr in gsi.get('AttributeDefinitions', []):
                        if attr not in create_params['AttributeDefinitions']:
                            create_params['AttributeDefinitions'].append(attr)
                
                create_params['GlobalSecondaryIndexes'] = gsi_config
            
            # Create the table
            table = dynamodb.create_table(**create_params)
            table.wait_until_exists()
        
        yield dynamodb


@pytest.fixture
def client(mock_dynamodb_tables):
    """Create a test client for FastAPI app"""
    return TestClient(test_app)


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing"""
    return {
        "CustomerCode": "TEST001",
        "CompanyName": "Test Company Ltd",
        "ContactFirstName": "John",
        "ContactLastName": "Doe", 
        "Email": "john.doe@testcompany.com",
        "Phone": "+1-555-0123",
        "Website": "https://testcompany.com",
        "IsActive": True
    }


@pytest.fixture
def sample_survey_data():
    """Sample survey data for testing"""
    return {
        "SurveyNumber": "SURV-2025-001",
        "SurveyTypeId": str(uuid.uuid4()),
        "CustomerId": str(uuid.uuid4()),
        "PropertyId": str(uuid.uuid4()),
        "SurveyStatusId": str(uuid.uuid4()),
        "EstimatedCost": 1500.00,
        "Notes": "Test survey for market research",
        "IsActive": True
    }


@pytest.fixture
def sample_property_data():
    """Sample property data for testing"""
    return {
        "PropertyCode": "PROP001",
        "PropertyName": "Test Property",
        "PropertyDescription": "A test commercial property",
        "OwnerName": "Property Owner LLC",
        "OwnerPhone": "+1-555-0456",
        "OwnerEmail": "owner@property.com",
        "IsActive": True
    }


@pytest.fixture
def created_customer(mock_dynamodb_tables, sample_customer_data):
    """Create a customer in the database for testing"""
    from crud import create_customer
    
    customer = Customer(**sample_customer_data)
    created = create_customer(customer)
    return created


@pytest.fixture
def created_survey(mock_dynamodb_tables, created_customer, sample_survey_data):
    """Create a survey in the database for testing"""
    from crud import create_survey
    
    # Update sample data with actual customer ID
    sample_survey_data["customer_id"] = created_customer.id
    survey = Survey(**sample_survey_data)
    created = create_survey(survey)
    return created


@pytest.fixture
def created_property(mock_dynamodb_tables, created_customer, sample_property_data):
    """Create a property in the database for testing"""
    from crud import create_property
    
    # Update sample data with actual customer ID
    sample_property_data["customer_id"] = created_customer.id
    property_obj = Property(**sample_property_data)
    created = create_property(property_obj)
    return created


@pytest.fixture
def mock_datetime():
    """Mock datetime for consistent testing"""
    test_datetime = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    with patch('models.datetime') as mock_dt:
        mock_dt.now.return_value = test_datetime
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        yield test_datetime


@pytest.fixture
def authenticated_headers():
    """Mock authentication headers for API tests"""
    return {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json"
    }


# Helper functions for tests
def assert_customer_equal(customer1: Customer, customer2: Customer):
    """Assert that two customers are equal"""
    assert customer1.CustomerCode == customer2.CustomerCode
    assert customer1.CompanyName == customer2.CompanyName
    assert customer1.Email == customer2.Email
    assert customer1.IsActive == customer2.IsActive


def assert_survey_equal(survey1: Survey, survey2: Survey):
    """Assert that two surveys are equal"""
    assert survey1.SurveyCode == survey2.SurveyCode
    assert survey1.customer_id == survey2.customer_id
    assert survey1.SurveyType == survey2.SurveyType
    assert survey1.Status == survey2.Status


def assert_property_equal(property1: Property, property2: Property):
    """Assert that two properties are equal"""
    assert property1.PropertyCode == property2.PropertyCode
    assert property1.customer_id == property2.customer_id
    assert property1.PropertyName == property2.PropertyName
    assert property1.PropertyType == property2.PropertyType


# Test data generators
def generate_customers(count: int = 5):
    """Generate multiple customer test data"""
    customers = []
    for i in range(count):
        customers.append({
            "CustomerCode": f"TEST{i:03d}",
            "CompanyName": f"Test Company {i}",
            "ContactPerson": f"Contact Person {i}",
            "Email": f"test{i}@company.com",
            "Phone": f"+1-555-{i:04d}",
            "Address": f"{i} Test Street",
            "City": f"Test City {i}",
            "State": "TS",
            "ZipCode": f"{12345 + i}",
            "Country": "Test Country",
            "IsActive": True
        })
    return customers


def generate_surveys(customer_ids: list, count: int = 3):
    """Generate multiple survey test data"""
    surveys = []
    for i, customer_id in enumerate(customer_ids[:count]):
        surveys.append({
            "SurveyCode": f"SURV{i:03d}",
            "customer_id": customer_id,
            "SurveyType": "Market Research",
            "Status": "Active",
            "StartDate": "2025-01-01",
            "EndDate": "2025-03-31",
            "Description": f"Test survey {i}",
            "IsActive": True
        })
    return surveys


def generate_properties(customer_ids: list, count: int = 3):
    """Generate multiple property test data"""
    properties = []
    for i, customer_id in enumerate(customer_ids[:count]):
        properties.append({
            "PropertyCode": f"PROP{i:03d}",
            "customer_id": customer_id,
            "PropertyName": f"Test Property {i}",
            "PropertyType": "Commercial",
            "Address": f"{i} Property Street",
            "City": f"Property City {i}",
            "State": "PS",
            "ZipCode": f"{54321 + i}",
            "Country": "Property Country",
            "SquareFootage": 5000.0 + (i * 100),
            "YearBuilt": 2020 + i,
            "IsActive": True
        })
    return properties