#!/usr/bin/env python3
"""
Test township creation directly with CRUD functions
"""
import os
import sys

# Set environment variables for local development
os.environ["AWS_ACCESS_KEY_ID"] = "fake"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["DYNAMODB_ENDPOINT"] = "http://localhost:8001"
os.environ["ENVIRONMENT"] = "local"

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from schemas import TownshipCreate
import crud

def test_create_township():
    """Test creating a township directly"""
    print("Testing township creation...")
    
    # Create test township data
    township_data = TownshipCreate(
        TownshipName="Test Township Direct",
        County="Test County",
        State="Test State"
    )
    
    try:
        # Test CRUD create function
        result = crud.create_township(township=township_data)
        print(f"✓ Township created successfully!")
        print(f"  Result: {result}")
        return result
    except Exception as e:
        print(f"✗ Error creating township: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_create_township()