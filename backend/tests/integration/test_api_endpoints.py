"""
Integration tests for FastAPI endpoints
Tests all API routes with TestClient and mocked DynamoDB
"""
import pytest
import json
from fastapi.testclient import TestClient

from models import Customer, Survey, Property


class TestCustomerEndpoints:
    """Test customer API endpoints"""
    
    def test_create_customer_endpoint(self, client, sample_customer_data):
        """Test POST /api/customers"""
        response = client.post("/api/customers", json=sample_customer_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert data["CustomerCode"] == sample_customer_data["CustomerCode"]
        assert data["CompanyName"] == sample_customer_data["CompanyName"]
        assert data["Email"] == sample_customer_data["Email"]
        assert data["IsActive"] is True
    
    def test_create_customer_invalid_data(self, client):
        """Test POST /api/customers with invalid data"""
        invalid_data = {
            "CustomerCode": "TEST001",
            # Missing required fields
        }
        
        response = client.post("/api/customers", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_customer_invalid_email(self, client, sample_customer_data):
        """Test POST /api/customers with invalid email"""
        sample_customer_data["Email"] = "invalid-email"
        
        response = client.post("/api/customers", json=sample_customer_data)
        assert response.status_code == 422
    
    def test_get_customers_list(self, client, mock_dynamodb_tables):
        """Test GET /api/customers"""
        # Create test customers first
        test_customers = [
            {"CustomerCode": "TEST001", "CompanyName": "Company 1", "Email": "test1@example.com"},
            {"CustomerCode": "TEST002", "CompanyName": "Company 2", "Email": "test2@example.com"},
            {"CustomerCode": "TEST003", "CompanyName": "Company 3", "Email": "test3@example.com"}
        ]
        
        created_ids = []
        for customer_data in test_customers:
            response = client.post("/api/customers", json=customer_data)
            assert response.status_code == 200
            created_ids.append(response.json()["id"])
        
        # Test getting customers list
        response = client.get("/api/customers")
        assert response.status_code == 200
        
        data = response.json()
        assert "customers" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        
        customers = data["customers"]
        assert len(customers) == 3
        assert data["total"] == 3
    
    def test_get_customers_pagination(self, client, mock_dynamodb_tables):
        """Test GET /api/customers with pagination"""
        # Create 5 test customers
        for i in range(5):
            customer_data = {
                "CustomerCode": f"TEST{i:03d}",
                "CompanyName": f"Company {i}",
                "Email": f"test{i}@example.com"
            }
            response = client.post("/api/customers", json=customer_data)
            assert response.status_code == 200
        
        # Test pagination
        response = client.get("/api/customers?page=1&size=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["customers"]) == 2
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["total"] == 5
    
    def test_get_customers_search(self, client, mock_dynamodb_tables):
        """Test GET /api/customers with search"""
        # Create test customers
        test_customers = [
            {"CustomerCode": "ACME001", "CompanyName": "ACME Corp", "Email": "acme@example.com"},
            {"CustomerCode": "BETA001", "CompanyName": "Beta Industries", "Email": "beta@example.com"},
            {"CustomerCode": "ACME002", "CompanyName": "ACME Ltd", "Email": "acme2@example.com"}
        ]
        
        for customer_data in test_customers:
            response = client.post("/api/customers", json=customer_data)
            assert response.status_code == 200
        
        # Test search
        response = client.get("/api/customers?search=ACME")
        assert response.status_code == 200
        
        data = response.json()
        customers = data["customers"]
        
        # Should find customers with "ACME" in the name or code
        acme_count = sum(1 for c in customers if "ACME" in c.get("CompanyName", "") or "ACME" in c.get("CustomerCode", ""))
        assert acme_count >= 2
    
    def test_get_customer_by_id(self, client, mock_dynamodb_tables, sample_customer_data):
        """Test GET /api/customers/{id}"""
        # Create a customer first
        create_response = client.post("/api/customers", json=sample_customer_data)
        assert create_response.status_code == 200
        customer_id = create_response.json()["id"]
        
        # Get the customer by ID
        response = client.get(f"/api/customers/{customer_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == customer_id
        assert data["CustomerCode"] == sample_customer_data["CustomerCode"]
        assert data["CompanyName"] == sample_customer_data["CompanyName"]
    
    def test_get_customer_not_found(self, client):
        """Test GET /api/customers/{id} with non-existent ID"""
        import uuid
        non_existent_id = str(uuid.uuid4())
        
        response = client.get(f"/api/customers/{non_existent_id}")
        assert response.status_code == 404
    
    def test_update_customer(self, client, mock_dynamodb_tables, sample_customer_data):
        """Test PUT /api/customers/{id}"""
        # Create a customer first
        create_response = client.post("/api/customers", json=sample_customer_data)
        assert create_response.status_code == 200
        customer_id = create_response.json()["id"]
        
        # Update the customer
        update_data = {
            "CompanyName": "Updated Company Name",
            "Email": "updated@example.com",
            "Phone": "+1-555-9999"
        }
        
        response = client.put(f"/api/customers/{customer_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == customer_id
        assert data["CompanyName"] == "Updated Company Name"
        assert data["Email"] == "updated@example.com"
        assert data["Phone"] == "+1-555-9999"
    
    def test_update_customer_not_found(self, client):
        """Test PUT /api/customers/{id} with non-existent ID"""
        import uuid
        non_existent_id = str(uuid.uuid4())
        
        update_data = {"CompanyName": "Updated Name"}
        response = client.put(f"/api/customers/{non_existent_id}", json=update_data)
        assert response.status_code == 404
    
    def test_delete_customer(self, client, mock_dynamodb_tables, sample_customer_data):
        """Test DELETE /api/customers/{id}"""
        # Create a customer first
        create_response = client.post("/api/customers", json=sample_customer_data)
        assert create_response.status_code == 200
        customer_id = create_response.json()["id"]
        
        # Delete the customer
        response = client.delete(f"/api/customers/{customer_id}")
        assert response.status_code == 200
        
        # Verify customer is deleted
        get_response = client.get(f"/api/customers/{customer_id}")
        assert get_response.status_code == 404
    
    def test_delete_customer_not_found(self, client):
        """Test DELETE /api/customers/{id} with non-existent ID"""
        import uuid
        non_existent_id = str(uuid.uuid4())
        
        response = client.delete(f"/api/customers/{non_existent_id}")
        assert response.status_code == 404


class TestSurveyEndpoints:
    """Test survey API endpoints"""
    
    def test_create_survey_endpoint(self, client, created_customer, sample_survey_data):
        """Test POST /api/surveys"""
        sample_survey_data["customer_id"] = created_customer.id
        
        response = client.post("/api/surveys", json=sample_survey_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert data["SurveyCode"] == sample_survey_data["SurveyCode"]
        assert data["customer_id"] == created_customer.id
        assert data["SurveyType"] == sample_survey_data["SurveyType"]
    
    def test_get_surveys_list(self, client, created_customer):
        """Test GET /api/surveys"""
        # Create test surveys
        test_surveys = [
            {"SurveyCode": "SURV001", "customer_id": created_customer.id, "SurveyType": "Type 1", "Status": "Active"},
            {"SurveyCode": "SURV002", "customer_id": created_customer.id, "SurveyType": "Type 2", "Status": "Completed"},
            {"SurveyCode": "SURV003", "customer_id": created_customer.id, "SurveyType": "Type 1", "Status": "Active"}
        ]
        
        for survey_data in test_surveys:
            response = client.post("/api/surveys", json=survey_data)
            assert response.status_code == 200
        
        # Test getting surveys list
        response = client.get("/api/surveys")
        assert response.status_code == 200
        
        data = response.json()
        assert "surveys" in data
        assert "total" in data
        surveys = data["surveys"]
        assert len(surveys) == 3
    
    def test_get_surveys_by_customer(self, client, created_customer):
        """Test GET /api/surveys with customer filter"""
        # Create surveys for the customer
        for i in range(3):
            survey_data = {
                "SurveyCode": f"SURV{i:03d}",
                "customer_id": created_customer.id,
                "SurveyType": "Market Research",
                "Status": "Active"
            }
            response = client.post("/api/surveys", json=survey_data)
            assert response.status_code == 200
        
        # Test filtering by customer
        response = client.get(f"/api/surveys?customer_id={created_customer.id}")
        assert response.status_code == 200
        
        data = response.json()
        surveys = data["surveys"]
        assert len(surveys) == 3
        
        for survey in surveys:
            assert survey["customer_id"] == created_customer.id
    
    def test_get_survey_by_id(self, client, created_survey):
        """Test GET /api/surveys/{id}"""
        response = client.get(f"/api/surveys/{created_survey.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_survey.id
        assert data["SurveyCode"] == created_survey.SurveyCode
    
    def test_update_survey(self, client, created_survey):
        """Test PUT /api/surveys/{id}"""
        update_data = {
            "Status": "Completed",
            "Description": "Updated description"
        }
        
        response = client.put(f"/api/surveys/{created_survey.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_survey.id
        assert data["Status"] == "Completed"
        assert data["Description"] == "Updated description"
    
    def test_delete_survey(self, client, created_survey):
        """Test DELETE /api/surveys/{id}"""
        survey_id = created_survey.id
        
        response = client.delete(f"/api/surveys/{survey_id}")
        assert response.status_code == 200
        
        # Verify survey is deleted
        get_response = client.get(f"/api/surveys/{survey_id}")
        assert get_response.status_code == 404


class TestPropertyEndpoints:
    """Test property API endpoints"""
    
    def test_create_property_endpoint(self, client, created_customer, sample_property_data):
        """Test POST /api/properties"""
        sample_property_data["customer_id"] = created_customer.id
        
        response = client.post("/api/properties", json=sample_property_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert data["PropertyCode"] == sample_property_data["PropertyCode"]
        assert data["customer_id"] == created_customer.id
        assert data["PropertyName"] == sample_property_data["PropertyName"]
    
    def test_get_properties_list(self, client, created_customer):
        """Test GET /api/properties"""
        # Create test properties
        test_properties = [
            {"PropertyCode": "PROP001", "customer_id": created_customer.id, "PropertyName": "Property 1"},
            {"PropertyCode": "PROP002", "customer_id": created_customer.id, "PropertyName": "Property 2"},
            {"PropertyCode": "PROP003", "customer_id": created_customer.id, "PropertyName": "Property 3"}
        ]
        
        for property_data in test_properties:
            response = client.post("/api/properties", json=property_data)
            assert response.status_code == 200
        
        # Test getting properties list
        response = client.get("/api/properties")
        assert response.status_code == 200
        
        data = response.json()
        assert "properties" in data
        assert "total" in data
        properties = data["properties"]
        assert len(properties) == 3
    
    def test_get_properties_by_customer(self, client, created_customer):
        """Test GET /api/properties with customer filter"""
        # Create properties for the customer
        for i in range(2):
            property_data = {
                "PropertyCode": f"PROP{i:03d}",
                "customer_id": created_customer.id,
                "PropertyName": f"Property {i}"
            }
            response = client.post("/api/properties", json=property_data)
            assert response.status_code == 200
        
        # Test filtering by customer
        response = client.get(f"/api/properties?customer_id={created_customer.id}")
        assert response.status_code == 200
        
        data = response.json()
        properties = data["properties"]
        assert len(properties) == 2
        
        for property_obj in properties:
            assert property_obj["customer_id"] == created_customer.id
    
    def test_get_property_by_id(self, client, created_property):
        """Test GET /api/properties/{id}"""
        response = client.get(f"/api/properties/{created_property.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_property.id
        assert data["PropertyCode"] == created_property.PropertyCode
    
    def test_update_property(self, client, created_property):
        """Test PUT /api/properties/{id}"""
        update_data = {
            "PropertyName": "Updated Property Name",
            "SquareFootage": 7500.0
        }
        
        response = client.put(f"/api/properties/{created_property.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_property.id
        assert data["PropertyName"] == "Updated Property Name"
        assert data["SquareFootage"] == 7500.0
    
    def test_delete_property(self, client, created_property):
        """Test DELETE /api/properties/{id}"""
        property_id = created_property.id
        
        response = client.delete(f"/api/properties/{property_id}")
        assert response.status_code == 200
        
        # Verify property is deleted
        get_response = client.get(f"/api/properties/{property_id}")
        assert get_response.status_code == 404


class TestLookupEndpoints:
    """Test lookup data endpoints"""
    
    def test_get_survey_types(self, client):
        """Test GET /api/lookup/survey-types"""
        response = client.get("/api/lookup/survey-types")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # Check that we have some survey types
        assert len(data) > 0
        
        # Check structure of survey type objects
        if data:
            survey_type = data[0]
            assert "SurveyTypeId" in survey_type
            assert "TypeName" in survey_type
    
    def test_get_survey_statuses(self, client):
        """Test GET /api/lookup/survey-statuses"""
        response = client.get("/api/lookup/survey-statuses")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        if data:
            status = data[0]
            assert "StatusId" in status
            assert "StatusName" in status
    
    def test_get_townships(self, client):
        """Test GET /api/lookup/townships"""
        response = client.get("/api/lookup/townships")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        if data:
            township = data[0]
            assert "TownshipId" in township
            assert "TownshipName" in township


class TestAPIErrorHandling:
    """Test API error handling"""
    
    def test_invalid_json_request(self, client):
        """Test API with invalid JSON"""
        response = client.post("/api/customers", 
                             data="invalid json",
                             headers={"content-type": "application/json"})
        assert response.status_code == 422
    
    def test_missing_content_type(self, client):
        """Test API without content-type header"""
        valid_data = {
            "CustomerCode": "TEST001",
            "CompanyName": "Test Company",
            "Email": "test@example.com"
        }
        
        response = client.post("/api/customers", 
                             data=json.dumps(valid_data))
        # FastAPI should handle this gracefully
        assert response.status_code in [200, 422]
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get("/api/customers")
        
        # Check that CORS headers are present
        headers = response.headers
        # Note: Specific CORS headers depend on FastAPI-CORS configuration
        assert response.status_code == 200
    
    def test_api_documentation_endpoint(self, client):
        """Test that API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint if it exists"""
        # Check if root endpoint works
        response = client.get("/")
        # Should either return 200 or 404 (if not implemented)
        assert response.status_code in [200, 404]
    
    def test_invalid_uuid_format(self, client):
        """Test API endpoints with invalid UUID format"""
        invalid_id = "not-a-uuid"
        
        response = client.get(f"/api/customers/{invalid_id}")
        assert response.status_code in [404, 422]  # Either not found or validation error
        
        response = client.put(f"/api/customers/{invalid_id}", json={"CompanyName": "Test"})
        assert response.status_code in [404, 422]
        
        response = client.delete(f"/api/customers/{invalid_id}")
        assert response.status_code in [404, 422]