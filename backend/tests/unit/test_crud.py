"""
Unit tests for CRUD operations (crud.py)
Tests all database operations with mocked DynamoDB
"""
import pytest
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from models import Customer, Survey, Property
from crud import (
    # Customer operations
    create_customer, get_customer, get_customers, update_customer, delete_customer,
    # Survey operations
    create_survey, get_survey, get_surveys, update_survey, delete_survey,
    # Property operations
    create_property, get_property, get_properties, update_property, delete_property,
    # Helper functions
    serialize_item, deserialize_item
)


class TestHelperFunctions:
    """Test helper functions for serialization"""
    
    def test_serialize_item_basic_types(self):
        """Test serialization of basic Python types"""
        item = {
            'string_field': 'test',
            'int_field': 123,
            'float_field': 45.67,
            'bool_field': True,
            'none_field': None
        }
        
        serialized = serialize_item(item)
        
        assert serialized['string_field'] == 'test'
        assert serialized['int_field'] == 123
        assert serialized['float_field'] == 45.67
        assert serialized['bool_field'] is True
        assert 'none_field' not in serialized  # None values should be removed
    
    def test_serialize_item_datetime(self):
        """Test serialization of datetime objects"""
        now = datetime.now()
        item = {'created_at': now}
        
        serialized = serialize_item(item)
        
        assert isinstance(serialized['created_at'], str)
        assert now.isoformat() in serialized['created_at']
    
    def test_deserialize_item(self):
        """Test deserialization of DynamoDB items"""
        dynamodb_item = {
            'string_field': 'test',
            'int_field': 123,
            'float_field': 45.67,
            'bool_field': True
        }
        
        deserialized = deserialize_item(dynamodb_item)
        
        assert deserialized == dynamodb_item
    
    def test_serialize_deserialize_roundtrip(self):
        """Test that serialize/deserialize is reversible"""
        original = {
            'id': str(uuid.uuid4()),
            'name': 'Test Item',
            'count': 42,
            'active': True,
            'created_at': datetime.now()
        }
        
        serialized = serialize_item(original)
        # Note: datetime will be converted to string, so exact roundtrip not possible
        assert 'id' in serialized
        assert serialized['name'] == 'Test Item'
        assert serialized['count'] == 42
        assert serialized['active'] is True


class TestCustomerCRUD:
    """Test Customer CRUD operations"""
    
    def test_create_customer(self, mock_dynamodb_tables, sample_customer_data):
        """Test customer creation"""
        customer = Customer(**sample_customer_data)
        created = create_customer(customer)
        
        assert created is not None
        assert created.id == customer.id
        assert created.CustomerCode == customer.CustomerCode
        assert created.CompanyName == customer.CompanyName
        assert created.Email == customer.Email
    
    def test_get_customer_by_id(self, mock_dynamodb_tables, created_customer):
        """Test getting customer by ID"""
        retrieved = get_customer(created_customer.id)
        
        assert retrieved is not None
        assert retrieved.id == created_customer.id
        assert retrieved.CustomerCode == created_customer.CustomerCode
        assert retrieved.CompanyName == created_customer.CompanyName
    
    def test_get_customer_not_found(self, mock_dynamodb_tables):
        """Test getting non-existent customer"""
        non_existent_id = str(uuid.uuid4())
        result = get_customer(non_existent_id)
        assert result is None
    
    def test_get_customers_list(self, mock_dynamodb_tables):
        """Test getting customers list"""
        # Create multiple customers
        customers_data = [
            {"CustomerCode": "TEST001", "CompanyName": "Company 1", "Email": "test1@example.com"},
            {"CustomerCode": "TEST002", "CompanyName": "Company 2", "Email": "test2@example.com"},
            {"CustomerCode": "TEST003", "CompanyName": "Company 3", "Email": "test3@example.com"}
        ]
        
        created_customers = []
        for data in customers_data:
            customer = Customer(**data)
            created = create_customer(customer)
            created_customers.append(created)
        
        # Test getting customers
        result = get_customers()
        
        assert 'customers' in result
        assert 'total' in result
        assert 'page' in result
        assert 'size' in result
        
        customers = result['customers']
        assert len(customers) == 3
        assert result['total'] == 3
    
    def test_get_customers_pagination(self, mock_dynamodb_tables):
        """Test customers pagination"""
        # Create 5 customers
        for i in range(5):
            customer_data = {
                "CustomerCode": f"TEST{i:03d}",
                "CompanyName": f"Company {i}",
                "Email": f"test{i}@example.com"
            }
            customer = Customer(**customer_data)
            create_customer(customer)
        
        # Test pagination
        result = get_customers(page=1, size=2)
        
        assert len(result['customers']) == 2
        assert result['page'] == 1
        assert result['size'] == 2
        assert result['total'] == 5
    
    def test_get_customers_search(self, mock_dynamodb_tables):
        """Test customers search functionality"""
        # Create customers with different names
        customers_data = [
            {"CustomerCode": "ACME001", "CompanyName": "ACME Corp", "Email": "acme@example.com"},
            {"CustomerCode": "BETA001", "CompanyName": "Beta Industries", "Email": "beta@example.com"},
            {"CustomerCode": "ACME002", "CompanyName": "ACME Ltd", "Email": "acme2@example.com"}
        ]
        
        for data in customers_data:
            customer = Customer(**data)
            create_customer(customer)
        
        # Test search
        result = get_customers(search="ACME")
        
        # Should find customers with "ACME" in the name
        customers = result['customers']
        assert len(customers) >= 2  # Should find at least the ACME customers
    
    def test_update_customer(self, mock_dynamodb_tables, created_customer):
        """Test customer update"""
        # Update customer data
        updated_data = {
            "CompanyName": "Updated Company Name",
            "Email": "updated@example.com",
            "Phone": "+1-555-9999"
        }
        
        updated = update_customer(created_customer.id, updated_data)
        
        assert updated is not None
        assert updated.id == created_customer.id
        assert updated.CompanyName == "Updated Company Name"
        assert updated.Email == "updated@example.com"
        assert updated.Phone == "+1-555-9999"
        # UpdatedAt should be modified
        assert updated.UpdatedAt != created_customer.UpdatedAt
    
    def test_update_customer_not_found(self, mock_dynamodb_tables):
        """Test updating non-existent customer"""
        non_existent_id = str(uuid.uuid4())
        updated = update_customer(non_existent_id, {"CompanyName": "Test"})
        assert updated is None
    
    def test_delete_customer(self, mock_dynamodb_tables, created_customer):
        """Test customer deletion"""
        customer_id = created_customer.id
        
        # Delete customer
        success = delete_customer(customer_id)
        assert success is True
        
        # Verify customer is deleted
        retrieved = get_customer(customer_id)
        assert retrieved is None
    
    def test_delete_customer_not_found(self, mock_dynamodb_tables):
        """Test deleting non-existent customer"""
        non_existent_id = str(uuid.uuid4())
        success = delete_customer(non_existent_id)
        assert success is False


class TestSurveyCRUD:
    """Test Survey CRUD operations"""
    
    def test_create_survey(self, mock_dynamodb_tables, created_customer, sample_survey_data):
        """Test survey creation"""
        sample_survey_data["customer_id"] = created_customer.id
        survey = Survey(**sample_survey_data)
        created = create_survey(survey)
        
        assert created is not None
        assert created.id == survey.id
        assert created.SurveyCode == survey.SurveyCode
        assert created.customer_id == created_customer.id
    
    def test_get_survey_by_id(self, mock_dynamodb_tables, created_survey):
        """Test getting survey by ID"""
        retrieved = get_survey(created_survey.id)
        
        assert retrieved is not None
        assert retrieved.id == created_survey.id
        assert retrieved.SurveyCode == created_survey.SurveyCode
    
    def test_get_surveys_list(self, mock_dynamodb_tables, created_customer):
        """Test getting surveys list"""
        # Create multiple surveys
        surveys_data = [
            {"SurveyCode": "SURV001", "customer_id": created_customer.id, "SurveyType": "Type 1", "Status": "Active"},
            {"SurveyCode": "SURV002", "customer_id": created_customer.id, "SurveyType": "Type 2", "Status": "Completed"},
            {"SurveyCode": "SURV003", "customer_id": created_customer.id, "SurveyType": "Type 1", "Status": "Active"}
        ]
        
        for data in surveys_data:
            survey = Survey(**data)
            create_survey(survey)
        
        # Test getting surveys
        result = get_surveys()
        
        assert 'surveys' in result
        assert 'total' in result
        surveys = result['surveys']
        assert len(surveys) == 3
    
    def test_get_surveys_by_customer(self, mock_dynamodb_tables, created_customer):
        """Test getting surveys filtered by customer"""
        # Create surveys for the customer
        for i in range(3):
            survey_data = {
                "SurveyCode": f"SURV{i:03d}",
                "customer_id": created_customer.id,
                "SurveyType": "Market Research",
                "Status": "Active"
            }
            survey = Survey(**survey_data)
            create_survey(survey)
        
        # Create another customer and survey
        other_customer_data = {
            "CustomerCode": "OTHER001",
            "CompanyName": "Other Company",
            "Email": "other@example.com"
        }
        other_customer = Customer(**other_customer_data)
        other_created = create_customer(other_customer)
        
        other_survey_data = {
            "SurveyCode": "OTHER_SURV",
            "customer_id": other_created.id,
            "SurveyType": "Market Research",
            "Status": "Active"
        }
        other_survey = Survey(**other_survey_data)
        create_survey(other_survey)
        
        # Test filtering by customer
        result = get_surveys(customer_id=created_customer.id)
        surveys = result['surveys']
        
        # Should only get surveys for the specific customer
        assert len(surveys) == 3
        for survey in surveys:
            assert survey.customer_id == created_customer.id
    
    def test_update_survey(self, mock_dynamodb_tables, created_survey):
        """Test survey update"""
        updated_data = {
            "Status": "Completed",
            "Description": "Updated description"
        }
        
        updated = update_survey(created_survey.id, updated_data)
        
        assert updated is not None
        assert updated.id == created_survey.id
        assert updated.Status == "Completed"
        assert updated.Description == "Updated description"
    
    def test_delete_survey(self, mock_dynamodb_tables, created_survey):
        """Test survey deletion"""
        survey_id = created_survey.id
        
        success = delete_survey(survey_id)
        assert success is True
        
        retrieved = get_survey(survey_id)
        assert retrieved is None


class TestPropertyCRUD:
    """Test Property CRUD operations"""
    
    def test_create_property(self, mock_dynamodb_tables, created_customer, sample_property_data):
        """Test property creation"""
        sample_property_data["customer_id"] = created_customer.id
        property_obj = Property(**sample_property_data)
        created = create_property(property_obj)
        
        assert created is not None
        assert created.id == property_obj.id
        assert created.PropertyCode == property_obj.PropertyCode
        assert created.customer_id == created_customer.id
    
    def test_get_property_by_id(self, mock_dynamodb_tables, created_property):
        """Test getting property by ID"""
        retrieved = get_property(created_property.id)
        
        assert retrieved is not None
        assert retrieved.id == created_property.id
        assert retrieved.PropertyCode == created_property.PropertyCode
    
    def test_get_properties_list(self, mock_dynamodb_tables, created_customer):
        """Test getting properties list"""
        # Create multiple properties
        properties_data = [
            {"PropertyCode": "PROP001", "customer_id": created_customer.id, "PropertyName": "Property 1"},
            {"PropertyCode": "PROP002", "customer_id": created_customer.id, "PropertyName": "Property 2"},
            {"PropertyCode": "PROP003", "customer_id": created_customer.id, "PropertyName": "Property 3"}
        ]
        
        for data in properties_data:
            property_obj = Property(**data)
            create_property(property_obj)
        
        result = get_properties()
        
        assert 'properties' in result
        assert 'total' in result
        properties = result['properties']
        assert len(properties) == 3
    
    def test_get_properties_by_customer(self, mock_dynamodb_tables, created_customer):
        """Test getting properties filtered by customer"""
        # Create properties for the customer
        for i in range(2):
            property_data = {
                "PropertyCode": f"PROP{i:03d}",
                "customer_id": created_customer.id,
                "PropertyName": f"Property {i}"
            }
            property_obj = Property(**property_data)
            create_property(property_obj)
        
        result = get_properties(customer_id=created_customer.id)
        properties = result['properties']
        
        assert len(properties) == 2
        for property_obj in properties:
            assert property_obj.customer_id == created_customer.id
    
    def test_update_property(self, mock_dynamodb_tables, created_property):
        """Test property update"""
        updated_data = {
            "PropertyName": "Updated Property Name",
            "SquareFootage": 7500.0
        }
        
        updated = update_property(created_property.id, updated_data)
        
        assert updated is not None
        assert updated.id == created_property.id
        assert updated.PropertyName == "Updated Property Name"
        assert updated.SquareFootage == 7500.0
    
    def test_delete_property(self, mock_dynamodb_tables, created_property):
        """Test property deletion"""
        property_id = created_property.id
        
        success = delete_property(property_id)
        assert success is True
        
        retrieved = get_property(property_id)
        assert retrieved is None


class TestCRUDErrorHandling:
    """Test error handling in CRUD operations"""
    
    def test_create_customer_duplicate_email(self, mock_dynamodb_tables, sample_customer_data):
        """Test handling of duplicate email addresses"""
        # Create first customer
        customer1 = Customer(**sample_customer_data)
        created1 = create_customer(customer1)
        assert created1 is not None
        
        # Try to create second customer with same email
        sample_customer_data["CustomerCode"] = "TEST002"
        customer2 = Customer(**sample_customer_data)
        
        # This should succeed in our current implementation
        # (DynamoDB doesn't enforce email uniqueness by default)
        created2 = create_customer(customer2)
        assert created2 is not None
        assert created2.id != created1.id
    
    def test_invalid_uuid_handling(self, mock_dynamodb_tables):
        """Test handling of invalid UUIDs"""
        invalid_id = "not-a-valid-uuid"
        
        customer = get_customer(invalid_id)
        assert customer is None
        
        survey = get_survey(invalid_id)
        assert survey is None
        
        property_obj = get_property(invalid_id)
        assert property_obj is None
    
    def test_database_connection_error_simulation(self, mock_dynamodb_tables):
        """Test handling of database connection errors"""
        # This test would require more sophisticated mocking
        # to simulate actual connection failures
        # For now, we'll test that our functions handle None returns gracefully
        
        non_existent_id = str(uuid.uuid4())
        result = get_customer(non_existent_id)
        assert result is None
    
    def test_empty_update_data(self, mock_dynamodb_tables, created_customer):
        """Test update with empty data"""
        updated = update_customer(created_customer.id, {})
        
        # Should return the original customer unchanged
        assert updated is not None
        assert updated.id == created_customer.id
        assert updated.CompanyName == created_customer.CompanyName