#!/usr/bin/env python3
"""
Check and create missing DynamoDB tables for Survey Types and Statuses
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import get_dynamodb
from backend.models import DYNAMODB_TABLES
import boto3

def check_and_create_tables():
    """Check if SurveyTypes and SurveyStatuses tables exist and create them if not"""
    
    # Get DynamoDB connection
    dynamodb = get_dynamodb()
    if dynamodb is None:
        print("❌ Could not connect to DynamoDB")
        return False
    
    # Tables we need for seeding
    required_tables = ['SurveyTypes', 'SurveyStatuses']
    
    try:
        # Get list of existing tables
        existing_tables = [table.name for table in dynamodb.tables.all()]
        print(f"Existing tables: {existing_tables}")
        
        for table_name in required_tables:
            if table_name in existing_tables:
                print(f"✅ Table '{table_name}' exists")
            else:
                print(f"❌ Table '{table_name}' does not exist. Creating...")
                create_table(dynamodb, table_name)
        
        return True
        
    except Exception as e:
        print(f"Error checking tables: {e}")
        return False

def create_table(dynamodb, table_name):
    """Create a DynamoDB table using the definition from models.py"""
    
    if table_name not in DYNAMODB_TABLES:
        print(f"❌ No table definition found for '{table_name}'")
        return False
    
    table_def = DYNAMODB_TABLES[table_name]
    
    try:
        table = dynamodb.create_table(
            TableName=table_def['TableName'],
            KeySchema=table_def['KeySchema'],
            AttributeDefinitions=table_def['AttributeDefinitions'],
            BillingMode='PAY_PER_REQUEST'  # Use on-demand billing for local dev
        )
        
        # Wait for table to be created
        table.wait_until_exists()
        print(f"✅ Successfully created table '{table_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Error creating table '{table_name}': {e}")
        return False

if __name__ == "__main__":
    print("============================================================")
    print("DynamoDB Table Check and Creation")
    print("============================================================")
    
    success = check_and_create_tables()
    
    if success:
        print("\n✅ All required tables are available")
    else:
        print("\n❌ Failed to ensure tables exist")
        sys.exit(1)