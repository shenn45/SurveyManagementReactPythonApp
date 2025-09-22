#!/usr/bin/env python3
"""
Test script to verify Graphene GraphQL integration
"""
import requests
import json

def test_graphql_endpoint():
    url = "http://localhost:8001/graphql"
    
    # Test simple customers query
    query = """
    query TestCustomers {
        customers(limit: 5) {
            customers {
                CustomerId
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
    
    response = requests.post(url, json={'query': query})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ GraphQL query successful!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        return True
    else:
        print(f"❌ GraphQL query failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_survey_types_query():
    url = "http://localhost:8001/graphql"
    
    # Test survey types query
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
    
    response = requests.post(url, json={'query': query})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Survey types query successful!")
        print(f"Response: {json.dumps(data, indent=2)}")
        return True
    else:
        print(f"❌ Survey types query failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_mutation():
    url = "http://localhost:8001/graphql"
    
    # Test customer creation mutation
    mutation = """
    mutation TestCreateCustomer {
        createCustomer(input: {
            CustomerCode: "TEST001"
            CompanyName: "Test Company"
            Email: "test@example.com"
            IsActive: true
        }) {
            customer {
                CustomerId
                CustomerCode
                CompanyName
                Email
                IsActive
            }
        }
    }
    """
    
    response = requests.post(url, json={'query': mutation})
    
    if response.status_code == 200:
        data = response.json()
        if 'errors' not in data:
            print("✅ GraphQL mutation successful!")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ GraphQL mutation had errors: {data['errors']}")
            return False
    else:
        print(f"❌ GraphQL mutation failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    print("Testing Graphene GraphQL Integration...")
    print("=" * 50)
    
    # Test queries
    print("\n1. Testing customers query...")
    test_graphql_endpoint()
    
    print("\n2. Testing survey types query...")
    test_survey_types_query()
    
    print("\n3. Testing customer creation mutation...")
    test_mutation()
    
    print("\n" + "=" * 50)
    print("Graphene GraphQL integration testing complete!")