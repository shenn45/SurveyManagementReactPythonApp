#!/usr/bin/env python3
"""
Simple township test without DynamoDB - using GraphQL endpoint directly
"""
import requests
import json

def test_township_graphql():
    """Test township operations via GraphQL"""
    
    graphql_url = "http://localhost:8000/graphql"
    
    # Test GraphQL query to get townships
    query = """
    query {
        townships(skip: 0, limit: 10) {
            townships {
                TownshipId
                TownshipName
                County
                State
                IsActive
                CreatedDate
            }
            total
        }
    }
    """
    
    try:
        response = requests.post(
            graphql_url,
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print("GraphQL errors:", data["errors"])
            else:
                townships_data = data.get("data", {}).get("townships", {})
                townships = townships_data.get("townships", [])
                total = townships_data.get("total", 0)
                
                print(f"✓ GraphQL query successful. Found {total} townships:")
                for township in townships:
                    print(f"  - {township['TownshipName']}, {township['County']} County, {township['State']}")
        else:
            print(f"✗ HTTP error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to GraphQL endpoint. Make sure the backend is running.")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test creating a township
    create_mutation = """
    mutation {
        create_township(input: {
            TownshipName: "Test Township"
            County: "Test County"
            State: "PA"
            IsActive: true
        }) {
            township {
                TownshipId
                TownshipName
                County
                State
                IsActive
            }
        }
    }
    """
    
    print("\nTesting township creation...")
    try:
        response = requests.post(
            graphql_url,
            json={"query": create_mutation},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print("GraphQL errors:", data["errors"])
            else:
                township = data.get("data", {}).get("create_township", {}).get("township")
                if township:
                    print(f"✓ Township created: {township['TownshipName']}, {township['County']} County, {township['State']}")
                else:
                    print("✗ Township creation returned empty result")
        else:
            print(f"✗ HTTP error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ Error creating township: {e}")

if __name__ == "__main__":
    test_township_graphql()