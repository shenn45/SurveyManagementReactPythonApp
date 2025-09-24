#!/usr/bin/env python3
"""
Test GraphQL UserSettings implementation
"""

import requests
import json

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

def test_upsert_user_settings():
    """Test creating/updating user settings via GraphQL"""
    
    # Test data for board settings
    board_settings = {
        "columnOrder": ["new", "in-progress", "completed", "delivered"],
        "hiddenColumns": ["archived"],
        "sortBy": "DueDate",
        "sortOrder": "asc"
    }
    
    # GraphQL mutation to upsert user settings
    mutation = """
    mutation UpsertUserSettings($input: UserSettingsInput!) {
        upsertUserSettings(input: $input) {
            userSettings {
                UserSettingsId
                UserId
                SettingsType
                SettingsData
                IsActive
                CreatedDate
                ModifiedDate
            }
        }
    }
    """
    
    variables = {
        "input": {
            "SettingsType": "BoardSettings",
            "SettingsData": json.dumps(board_settings)
        }
    }
    
    payload = {
        "query": mutation,
        "variables": variables
    }
    
    print("Testing upsertUserSettings mutation...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return False
        
        user_settings = result.get("data", {}).get("upsertUserSettings", {}).get("userSettings")
        if user_settings:
            print("✅ UserSettings upserted successfully!")
            return user_settings
        else:
            print("❌ Failed to upsert user settings")
            return False
            
    except Exception as e:
        print(f"❌ Error testing upsert: {e}")
        return False

def test_query_user_settings(settings_type="BoardSettings"):
    """Test querying user settings via GraphQL"""
    
    # GraphQL query to get user settings
    query = """
    query GetUserSettings($settingsType: String!) {
        userSettings(settingsType: $settingsType) {
            UserSettingsId
            UserId
            SettingsType
            SettingsData
            IsActive
            CreatedDate
            ModifiedDate
        }
    }
    """
    
    variables = {
        "settingsType": settings_type
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    print(f"\nTesting userSettings query for type: {settings_type}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return False
        
        user_settings = result.get("data", {}).get("userSettings")
        if user_settings:
            print("✅ UserSettings queried successfully!")
            
            # Parse and display the settings data
            settings_data = json.loads(user_settings.get("SettingsData", "{}"))
            print(f"📋 Parsed Settings Data: {json.dumps(settings_data, indent=2)}")
            
            return user_settings
        else:
            print("ℹ️  No user settings found")
            return None
            
    except Exception as e:
        print(f"❌ Error testing query: {e}")
        return False

def test_query_all_user_settings():
    """Test querying all user settings via GraphQL"""
    
    # GraphQL query to get all user settings
    query = """
    query GetAllUserSettings {
        allUserSettings {
            UserSettingsId
            UserId
            SettingsType
            SettingsData
            IsActive
            CreatedDate
            ModifiedDate
        }
    }
    """
    
    payload = {
        "query": query
    }
    
    print(f"\nTesting allUserSettings query...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return False
        
        all_settings = result.get("data", {}).get("allUserSettings", [])
        print(f"✅ Found {len(all_settings)} user settings")
        
        return all_settings
            
    except Exception as e:
        print(f"❌ Error testing query: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing GraphQL UserSettings Implementation")
    print("=" * 50)
    
    # Test 1: Create/Update user settings
    upserted_settings = test_upsert_user_settings()
    
    # Test 2: Query specific user settings
    if upserted_settings:
        queried_settings = test_query_user_settings("BoardSettings")
    
    # Test 3: Query all user settings
    all_settings = test_query_all_user_settings()
    
    print("\n" + "=" * 50)
    print("🏁 GraphQL UserSettings tests completed!")