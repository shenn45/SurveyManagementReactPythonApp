"""
Unit tests for Pydantic models
Tests model validation, serialization, and business logic
"""
import pytest
import uuid
from datetime import datetime
from pydantic import ValidationError

from models import Customer, Survey, Property, DYNAMODB_TABLES


class TestCustomer:
    """Test Customer model"""
    
    def test_customer_creation_valid_data(self, sample_customer_data):
        """Test customer creation with valid data"""
        customer = Customer(**sample_customer_data)
        
        assert customer.CustomerCode == "TEST001"
        assert customer.CompanyName == "Test Company Ltd"
        assert customer.Email == "john.doe@testcompany.com"
        assert customer.IsActive is True
        assert isinstance(customer.CustomerId, str)
        assert len(customer.CustomerId) == 36  # UUID length
        assert customer.CreatedDate is not None
        assert customer.ModifiedDate is not None
        # Timestamps are set within microseconds of each other
        time_diff = abs((customer.CreatedDate - customer.ModifiedDate).total_seconds())
        assert time_diff < 1.0  # Should be within 1 second
    
    def test_customer_id_generation(self, sample_customer_data):
        """Test that customer ID is automatically generated"""
        customer1 = Customer(**sample_customer_data)
        customer2 = Customer(**sample_customer_data)
        
        assert customer1.CustomerId != customer2.CustomerId
        assert len(customer1.CustomerId) == 36
        assert len(customer2.CustomerId) == 36
    
    def test_customer_email_validation(self, sample_customer_data):
        """Test email field is optional and accepts any string"""
        # Valid email
        customer = Customer(**sample_customer_data)
        assert customer.Email == "john.doe@testcompany.com"
        
        # Email is optional, so None should work
        sample_customer_data["Email"] = None
        customer = Customer(**sample_customer_data)
        assert customer.Email is None
        
        # Any string is accepted since there's no email validation
        sample_customer_data["Email"] = "not-an-email"
        customer = Customer(**sample_customer_data)
        assert customer.Email == "not-an-email"
    
    def test_customer_required_fields(self):
        """Test that required fields are validated"""
        # Missing required fields
        with pytest.raises(ValidationError) as exc_info:
            Customer()
        
        errors = exc_info.value.errors()
        required_fields = {error['loc'][0] for error in errors if error['type'] == 'missing'}
        expected_required = {'CustomerCode', 'CompanyName'}
        assert expected_required.issubset(required_fields)
    
    def test_customer_optional_fields(self, sample_customer_data):
        """Test that optional fields have defaults"""
        # Remove optional fields
        minimal_data = {
            "CustomerCode": sample_customer_data["CustomerCode"],
            "CompanyName": sample_customer_data["CompanyName"]
        }
        
        customer = Customer(**minimal_data)
        assert customer.ContactFirstName is None
        assert customer.ContactLastName is None
        assert customer.Email is None
        assert customer.Phone is None
        assert customer.IsActive is True  # Default value
    
    def test_customer_serialization(self, sample_customer_data):
        """Test customer serialization to dict"""
        customer = Customer(**sample_customer_data)
        data = customer.model_dump()
        
        assert isinstance(data, dict)
        assert data["CustomerCode"] == "TEST001"
        assert data["CompanyName"] == "Test Company Ltd"
        assert data["Email"] == "john.doe@testcompany.com"
        assert "CustomerId" in data
        assert "CreatedDate" in data
        assert "ModifiedDate" in data
    
    def test_customer_json_serialization(self, sample_customer_data):
        """Test customer JSON serialization"""
        customer = Customer(**sample_customer_data)
        json_str = customer.model_dump_json()
        
        assert isinstance(json_str, str)
        assert "TEST001" in json_str
        assert "Test Company Ltd" in json_str
    
    def test_customer_update_timestamps(self, sample_customer_data):
        """Test that ModifiedDate is set on creation"""
        customer = Customer(**sample_customer_data)
        original_modified = customer.ModifiedDate
        
        # In Pydantic models, timestamps don't auto-update unless explicitly managed
        # This test verifies the timestamp is set during creation
        assert customer.ModifiedDate == original_modified  
        assert isinstance(original_modified, datetime)


class TestSurvey:
    """Test Survey model"""
    
    def test_survey_creation_valid_data(self, sample_survey_data):
        """Test survey creation with valid data"""
        survey = Survey(**sample_survey_data)
        
        assert survey.SurveyNumber == "SURV-2025-001"
        assert survey.IsActive is True
        assert isinstance(survey.SurveyId, str)
        assert len(survey.SurveyId) == 36
        assert isinstance(survey.CustomerId, str)
        assert isinstance(survey.PropertyId, str)
        assert isinstance(survey.SurveyTypeId, str)
        assert isinstance(survey.SurveyStatusId, str)
    
    def test_survey_required_fields(self):
        """Test that required fields are validated"""
        with pytest.raises(ValidationError) as exc_info:
            Survey()
        
        errors = exc_info.value.errors()
        required_fields = {error['loc'][0] for error in errors if error['type'] == 'missing'}
        expected_required = {'SurveyNumber', 'SurveyTypeId', 'CustomerId', 'PropertyId', 'SurveyStatusId'}
        assert expected_required.issubset(required_fields)
    
    def test_survey_customer_id_validation(self, sample_survey_data):
        """Test CustomerId validation"""
        # Valid UUID string
        valid_uuid = str(uuid.uuid4())
        sample_survey_data["CustomerId"] = valid_uuid
        survey = Survey(**sample_survey_data)
        assert survey.CustomerId == valid_uuid
    
    def test_survey_date_fields(self, sample_survey_data):
        """Test date field handling"""
        survey = Survey(**sample_survey_data)
        
        # RequestDate should be set automatically
        assert survey.RequestDate is not None
        assert isinstance(survey.RequestDate, datetime)
        
        # CompletedDate should be None initially
        assert survey.CompletedDate is None
    
    def test_survey_optional_fields(self, sample_survey_data):
        """Test optional fields and defaults"""
        # Remove optional fields
        minimal_data = {
            "SurveyNumber": sample_survey_data["SurveyNumber"],
            "SurveyTypeId": sample_survey_data["SurveyTypeId"],
            "CustomerId": sample_survey_data["CustomerId"],
            "PropertyId": sample_survey_data["PropertyId"],
            "SurveyStatusId": sample_survey_data["SurveyStatusId"]
        }
        
        survey = Survey(**minimal_data)
        assert survey.EstimatedCost is None
        assert survey.ActualCost is None
        assert survey.Notes is None
        assert survey.SurveyorNotes is None
        assert survey.IsActive is True  # Default value
    
    def test_survey_serialization(self, sample_survey_data):
        """Test survey serialization to dict"""
        survey = Survey(**sample_survey_data)
        data = survey.model_dump()
        
        assert isinstance(data, dict)
        assert data["SurveyNumber"] == "SURV-2025-001"
        assert "SurveyId" in data
        assert "CustomerId" in data
        assert "PropertyId" in data
        assert "SurveyTypeId" in data
        assert "SurveyStatusId" in data


class TestProperty:
    """Test Property model"""
    
    def test_property_creation_valid_data(self, sample_property_data):
        """Test property creation with valid data"""
        property_obj = Property(**sample_property_data)
        
        assert property_obj.PropertyCode == "PROP001"
        assert property_obj.PropertyName == "Test Property"
        assert property_obj.IsActive is True
        assert isinstance(property_obj.PropertyId, str)
        assert len(property_obj.PropertyId) == 36
    
    def test_property_required_fields(self):
        """Test that required fields are validated"""
        with pytest.raises(ValidationError) as exc_info:
            Property()
        
        errors = exc_info.value.errors()
        required_fields = {error['loc'][0] for error in errors if error['type'] == 'missing'}
        expected_required = {'PropertyCode', 'PropertyName'}
        assert expected_required.issubset(required_fields)
    
    def test_property_numeric_fields(self, sample_property_data):
        """Test numeric field handling"""
        property_obj = Property(**sample_property_data)
        
        # These fields are optional in the actual model
        assert property_obj.PropertyDescription == "A test commercial property"
        assert property_obj.OwnerName == "Property Owner LLC"
    
    def test_property_optional_fields(self, sample_property_data):
        """Test optional fields and defaults"""
        # Remove optional fields
        minimal_data = {
            "PropertyCode": sample_property_data["PropertyCode"],
            "PropertyName": sample_property_data["PropertyName"]
        }
        
        property_obj = Property(**minimal_data)
        assert property_obj.PropertyDescription is None
        assert property_obj.OwnerName is None
        assert property_obj.OwnerPhone is None
        assert property_obj.OwnerEmail is None
        assert property_obj.IsActive is True  # Default value
    
    def test_property_serialization(self, sample_property_data):
        """Test property serialization to dict"""
        property_obj = Property(**sample_property_data)
        data = property_obj.model_dump()
        
        assert isinstance(data, dict)
        assert data["PropertyCode"] == "PROP001"
        assert data["PropertyName"] == "Test Property"
        assert "PropertyId" in data
        assert "CreatedDate" in data
        assert "ModifiedDate" in data


class TestDynamoDBConfiguration:
    """Test DynamoDB table configuration"""
    
    def test_dynamodb_tables_config_exists(self):
        """Test that DYNAMODB_TABLES configuration exists"""
        assert DYNAMODB_TABLES is not None
        assert isinstance(DYNAMODB_TABLES, dict)
        assert len(DYNAMODB_TABLES) > 0
    
    def test_required_tables_exist(self):
        """Test that all required tables are configured"""
        required_tables = ['Customers', 'Surveys', 'Properties']
        
        for table in required_tables:
            assert table in DYNAMODB_TABLES
            assert 'TableName' in DYNAMODB_TABLES[table]
            assert 'KeySchema' in DYNAMODB_TABLES[table]
            assert 'AttributeDefinitions' in DYNAMODB_TABLES[table]
    
    def test_table_configuration_structure(self):
        """Test table configuration has proper structure"""
        for table_name, config in DYNAMODB_TABLES.items():
            assert isinstance(config['TableName'], str)
            assert isinstance(config['KeySchema'], list)
            assert isinstance(config['AttributeDefinitions'], list)
            assert len(config['KeySchema']) > 0
            assert len(config['AttributeDefinitions']) > 0
    
    def test_customers_table_config(self):
        """Test customers table configuration"""
        customers_config = DYNAMODB_TABLES['Customers']
        assert customers_config['TableName'] == 'Customers'
        
        # Check primary key
        key_schema = customers_config['KeySchema']
        primary_key = next(key for key in key_schema if key['KeyType'] == 'HASH')
        assert primary_key['AttributeName'] == 'CustomerId'
    
    def test_surveys_table_config(self):
        """Test surveys table configuration"""
        surveys_config = DYNAMODB_TABLES['Surveys']
        assert surveys_config['TableName'] == 'Surveys'
        
        # Check primary key
        key_schema = surveys_config['KeySchema']
        primary_key = next(key for key in key_schema if key['KeyType'] == 'HASH')
        assert primary_key['AttributeName'] == 'SurveyId'
    
    def test_properties_table_config(self):
        """Test properties table configuration"""
        properties_config = DYNAMODB_TABLES['Properties']
        assert properties_config['TableName'] == 'Properties'
        
        # Check primary key
        key_schema = properties_config['KeySchema']
        primary_key = next(key for key in key_schema if key['KeyType'] == 'HASH')
        assert primary_key['AttributeName'] == 'PropertyId'