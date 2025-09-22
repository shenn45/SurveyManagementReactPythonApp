"""
Integration tests for GraphQL endpoints
Tests GraphQL queries and mutations with mocked DynamoDB
"""
import pytest
import json
from fastapi.testclient import TestClient


class TestGraphQLCustomerQueries:
    """Test GraphQL customer queries"""
    
    def test_customers_query(self, client, mock_dynamodb_tables):
        """Test GraphQL customers query"""
        # Create test customers first
        test_customers = [
            {"CustomerCode": "TEST001", "CompanyName": "Company 1", "Email": "test1@example.com"},
            {"CustomerCode": "TEST002", "CompanyName": "Company 2", "Email": "test2@example.com"}
        ]
        
        for customer_data in test_customers:
            response = client.post("/api/customers", json=customer_data)
            assert response.status_code == 200
        
        # Test GraphQL query
        query = """
        query TestCustomers {
            customers(limit: 10) {
                customers {
                    id
                    CustomerCode
                    CompanyName
                    Email
                    IsActive
                }
                total
                page
                size
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "customers" in data["data"]
        
        customers_result = data["data"]["customers"]
        assert "customers" in customers_result
        assert "total" in customers_result
        assert len(customers_result["customers"]) == 2
        assert customers_result["total"] == 2
    
    def test_customer_by_id_query(self, client, created_customer):
        """Test GraphQL customer by ID query"""
        query = f"""
        query TestCustomer {{
            customer(id: "{created_customer.id}") {{
                id
                CustomerCode
                CompanyName
                Email
                IsActive
                CreatedAt
                UpdatedAt
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "customer" in data["data"]
        
        customer = data["data"]["customer"]
        assert customer["id"] == created_customer.id
        assert customer["CustomerCode"] == created_customer.CustomerCode
        assert customer["CompanyName"] == created_customer.CompanyName
    
    def test_customers_pagination_query(self, client, mock_dynamodb_tables):
        """Test GraphQL customers pagination"""
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
        query = """
        query TestCustomersPagination {
            customers(limit: 2, offset: 2) {
                customers {
                    CustomerCode
                    CompanyName
                }
                total
                page
                size
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        customers_result = data["data"]["customers"]
        assert len(customers_result["customers"]) <= 2
        assert customers_result["total"] == 5
    
    def test_customer_not_found_query(self, client):
        """Test GraphQL customer query with non-existent ID"""
        import uuid
        non_existent_id = str(uuid.uuid4())
        
        query = f"""
        query TestCustomerNotFound {{
            customer(id: "{non_existent_id}") {{
                id
                CustomerCode
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        assert data["data"]["customer"] is None


class TestGraphQLCustomerMutations:
    """Test GraphQL customer mutations"""
    
    def test_create_customer_mutation(self, client, mock_dynamodb_tables, sample_customer_data):
        """Test GraphQL createCustomer mutation"""
        mutation = f"""
        mutation TestCreateCustomer {{
            createCustomer(input: {{
                CustomerCode: "{sample_customer_data['CustomerCode']}"
                CompanyName: "{sample_customer_data['CompanyName']}"
                ContactPerson: "{sample_customer_data['ContactPerson']}"
                Email: "{sample_customer_data['Email']}"
                Phone: "{sample_customer_data['Phone']}"
                Address: "{sample_customer_data['Address']}"
                City: "{sample_customer_data['City']}"
                State: "{sample_customer_data['State']}"
                ZipCode: "{sample_customer_data['ZipCode']}"
                Country: "{sample_customer_data['Country']}"
                IsActive: {str(sample_customer_data['IsActive']).lower()}
            }}) {{
                customer {{
                    id
                    CustomerCode
                    CompanyName
                    Email
                    IsActive
                }}
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "createCustomer" in data["data"]
        
        customer = data["data"]["createCustomer"]["customer"]
        assert "id" in customer
        assert customer["CustomerCode"] == sample_customer_data["CustomerCode"]
        assert customer["CompanyName"] == sample_customer_data["CompanyName"]
        assert customer["Email"] == sample_customer_data["Email"]
    
    def test_update_customer_mutation(self, client, created_customer):
        """Test GraphQL updateCustomer mutation"""
        mutation = f"""
        mutation TestUpdateCustomer {{
            updateCustomer(
                id: "{created_customer.id}"
                input: {{
                    CompanyName: "Updated Company Name"
                    Email: "updated@example.com"
                    Phone: "+1-555-9999"
                }}
            ) {{
                customer {{
                    id
                    CustomerCode
                    CompanyName
                    Email
                    Phone
                }}
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        
        data = response.json()
        customer = data["data"]["updateCustomer"]["customer"]
        assert customer["id"] == created_customer.id
        assert customer["CompanyName"] == "Updated Company Name"
        assert customer["Email"] == "updated@example.com"
        assert customer["Phone"] == "+1-555-9999"
    
    def test_delete_customer_mutation(self, client, created_customer):
        """Test GraphQL deleteCustomer mutation"""
        mutation = f"""
        mutation TestDeleteCustomer {{
            deleteCustomer(id: "{created_customer.id}") {{
                success
                message
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        
        data = response.json()
        result = data["data"]["deleteCustomer"]
        assert result["success"] is True
        
        # Verify customer is deleted
        query = f"""
        query VerifyDeleted {{
            customer(id: "{created_customer.id}") {{
                id
            }}
        }}
        """
        
        verify_response = client.post("/graphql", json={"query": query})
        verify_data = verify_response.json()
        assert verify_data["data"]["customer"] is None


class TestGraphQLSurveyQueries:
    """Test GraphQL survey queries"""
    
    def test_surveys_query(self, client, created_customer):
        """Test GraphQL surveys query"""
        # Create test surveys
        test_surveys = [
            {"SurveyCode": "SURV001", "customer_id": created_customer.id, "SurveyType": "Type 1", "Status": "Active"},
            {"SurveyCode": "SURV002", "customer_id": created_customer.id, "SurveyType": "Type 2", "Status": "Completed"}
        ]
        
        for survey_data in test_surveys:
            response = client.post("/api/surveys", json=survey_data)
            assert response.status_code == 200
        
        # Test GraphQL query
        query = """
        query TestSurveys {
            surveys(limit: 10) {
                surveys {
                    id
                    SurveyCode
                    customer_id
                    SurveyType
                    Status
                    IsActive
                }
                total
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        surveys_result = data["data"]["surveys"]
        assert len(surveys_result["surveys"]) == 2
        assert surveys_result["total"] == 2
    
    def test_surveys_by_customer_query(self, client, created_customer):
        """Test GraphQL surveys by customer query"""
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
        query = f"""
        query TestSurveysByCustomer {{
            surveys(customerId: "{created_customer.id}") {{
                surveys {{
                    id
                    SurveyCode
                    customer_id
                }}
                total
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        surveys_result = data["data"]["surveys"]
        surveys = surveys_result["surveys"]
        
        assert len(surveys) == 3
        for survey in surveys:
            assert survey["customer_id"] == created_customer.id
    
    def test_survey_by_id_query(self, client, created_survey):
        """Test GraphQL survey by ID query"""
        query = f"""
        query TestSurvey {{
            survey(id: "{created_survey.id}") {{
                id
                SurveyCode
                customer_id
                SurveyType
                Status
                StartDate
                EndDate
                Description
                IsActive
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        survey = data["data"]["survey"]
        assert survey["id"] == created_survey.id
        assert survey["SurveyCode"] == created_survey.SurveyCode


class TestGraphQLSurveyMutations:
    """Test GraphQL survey mutations"""
    
    def test_create_survey_mutation(self, client, created_customer, sample_survey_data):
        """Test GraphQL createSurvey mutation"""
        mutation = f"""
        mutation TestCreateSurvey {{
            createSurvey(input: {{
                SurveyCode: "{sample_survey_data['SurveyCode']}"
                customer_id: "{created_customer.id}"
                SurveyType: "{sample_survey_data['SurveyType']}"
                Status: "{sample_survey_data['Status']}"
                StartDate: "{sample_survey_data['StartDate']}"
                EndDate: "{sample_survey_data['EndDate']}"
                Description: "{sample_survey_data['Description']}"
                IsActive: {str(sample_survey_data['IsActive']).lower()}
            }}) {{
                survey {{
                    id
                    SurveyCode
                    customer_id
                    SurveyType
                    Status
                }}
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        
        data = response.json()
        survey = data["data"]["createSurvey"]["survey"]
        assert "id" in survey
        assert survey["SurveyCode"] == sample_survey_data["SurveyCode"]
        assert survey["customer_id"] == created_customer.id
    
    def test_update_survey_mutation(self, client, created_survey):
        """Test GraphQL updateSurvey mutation"""
        mutation = f"""
        mutation TestUpdateSurvey {{
            updateSurvey(
                id: "{created_survey.id}"
                input: {{
                    Status: "Completed"
                    Description: "Updated description"
                }}
            ) {{
                survey {{
                    id
                    Status
                    Description
                }}
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        
        data = response.json()
        survey = data["data"]["updateSurvey"]["survey"]
        assert survey["id"] == created_survey.id
        assert survey["Status"] == "Completed"
        assert survey["Description"] == "Updated description"
    
    def test_delete_survey_mutation(self, client, created_survey):
        """Test GraphQL deleteSurvey mutation"""
        mutation = f"""
        mutation TestDeleteSurvey {{
            deleteSurvey(id: "{created_survey.id}") {{
                success
                message
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        
        data = response.json()
        result = data["data"]["deleteSurvey"]
        assert result["success"] is True


class TestGraphQLPropertyQueries:
    """Test GraphQL property queries"""
    
    def test_properties_query(self, client, created_customer):
        """Test GraphQL properties query"""
        # Create test properties
        test_properties = [
            {"PropertyCode": "PROP001", "customer_id": created_customer.id, "PropertyName": "Property 1"},
            {"PropertyCode": "PROP002", "customer_id": created_customer.id, "PropertyName": "Property 2"}
        ]
        
        for property_data in test_properties:
            response = client.post("/api/properties", json=property_data)
            assert response.status_code == 200
        
        # Test GraphQL query
        query = """
        query TestProperties {
            properties(limit: 10) {
                properties {
                    id
                    PropertyCode
                    customer_id
                    PropertyName
                    PropertyType
                    SquareFootage
                    YearBuilt
                    IsActive
                }
                total
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        properties_result = data["data"]["properties"]
        assert len(properties_result["properties"]) == 2
        assert properties_result["total"] == 2
    
    def test_property_by_id_query(self, client, created_property):
        """Test GraphQL property by ID query"""
        query = f"""
        query TestProperty {{
            property(id: "{created_property.id}") {{
                id
                PropertyCode
                customer_id
                PropertyName
                PropertyType
                Address
                City
                State
                ZipCode
                Country
                SquareFootage
                YearBuilt
                IsActive
            }}
        }}
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        property_obj = data["data"]["property"]
        assert property_obj["id"] == created_property.id
        assert property_obj["PropertyCode"] == created_property.PropertyCode


class TestGraphQLLookupQueries:
    """Test GraphQL lookup queries"""
    
    def test_survey_types_query(self, client):
        """Test GraphQL surveyTypes query"""
        query = """
        query TestSurveyTypes {
            surveyTypes {
                SurveyTypeId
                TypeName
                TypeDescription
                IsActive
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        assert "surveyTypes" in data["data"]
        survey_types = data["data"]["surveyTypes"]
        assert isinstance(survey_types, list)
        assert len(survey_types) > 0
    
    def test_survey_statuses_query(self, client):
        """Test GraphQL surveyStatuses query"""
        query = """
        query TestSurveyStatuses {
            surveyStatuses {
                StatusId
                StatusName
                StatusDescription
                IsActive
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        assert "surveyStatuses" in data["data"]
        statuses = data["data"]["surveyStatuses"]
        assert isinstance(statuses, list)
        assert len(statuses) > 0
    
    def test_townships_query(self, client):
        """Test GraphQL townships query"""
        query = """
        query TestTownships {
            townships {
                TownshipId
                TownshipName
                County
                State
                IsActive
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        
        data = response.json()
        assert "townships" in data["data"]
        townships = data["data"]["townships"]
        assert isinstance(townships, list)
        assert len(townships) > 0


class TestGraphQLErrorHandling:
    """Test GraphQL error handling"""
    
    def test_invalid_query_syntax(self, client):
        """Test GraphQL with invalid syntax"""
        invalid_query = """
        query InvalidSyntax {
            customers {
                missing_closing_brace
        """
        
        response = client.post("/graphql", json={"query": invalid_query})
        assert response.status_code == 400
        
        data = response.json()
        assert "errors" in data
    
    def test_nonexistent_field_query(self, client):
        """Test GraphQL query with non-existent field"""
        query = """
        query TestNonExistentField {
            customers {
                customers {
                    nonExistentField
                }
            }
        }
        """
        
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 400
        
        data = response.json()
        assert "errors" in data
    
    def test_invalid_mutation_input(self, client):
        """Test GraphQL mutation with invalid input"""
        mutation = """
        mutation TestInvalidInput {
            createCustomer(input: {
                CustomerCode: "TEST001"
                # Missing required fields
            }) {
                customer {
                    id
                }
            }
        }
        """
        
        response = client.post("/graphql", json={"query": mutation})
        # Should return error for missing required fields
        data = response.json()
        assert "errors" in data or response.status_code != 200
    
    def test_graphql_introspection(self, client):
        """Test GraphQL introspection query"""
        introspection_query = """
        query IntrospectionQuery {
            __schema {
                types {
                    name
                    kind
                }
            }
        }
        """
        
        response = client.post("/graphql", json={"query": introspection_query})
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "__schema" in data["data"]
        assert "types" in data["data"]["__schema"]