#!/usr/bin/env python3
"""
Quick table creation and verification script
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_dynamodb
from models import DYNAMODB_TABLES
import boto3

def setup_local_tables():
    """Setup tables for local DynamoDB development"""
    
    # Connect to local DynamoDB
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8001',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
            region_name='us-east-1'
        )
        
        print("Connected to local DynamoDB at http://localhost:8001")
        
        # Check existing tables
        existing_tables = list(dynamodb.tables.all())
        existing_table_names = [table.name for table in existing_tables]
        print(f"Existing tables: {existing_table_names}")
        
        # Define required tables with their key attributes
        required_tables = [
            'Customers',
            'Surveys', 
            'Properties',
            'Townships',
            'SurveyTypes',
            'SurveyStatuses'
        ]
        
        # Create missing tables
        for table_name in required_tables:
            if table_name not in existing_table_names:
                try:
                    print(f"Creating table: {table_name}")
                    create_table(dynamodb, table_name)
                    print(f"✓ Table {table_name} created successfully")
                    
                except Exception as e:
                    print(f"✗ Error creating table {table_name}: {e}")
            else:
                print(f"✓ Table {table_name} already exists")
        
        print("\n✅ All tables are ready!")
        return True
        
    except Exception as e:
        print(f"✗ Error connecting to DynamoDB: {e}")
        print("Make sure moto server is running: python -m moto.server -p 8001 -H 0.0.0.0")
        return False

def create_table(dynamodb, table_name):
    """Create a DynamoDB table using the definition from models.py"""
    
    if table_name not in DYNAMODB_TABLES:
        print(f"❌ No table definition found for '{table_name}'")
        return False
    
    table_def = DYNAMODB_TABLES[table_name]
    
    try:
        # Create table with basic configuration (without GSIs for simplicity)
        table = dynamodb.create_table(
            TableName=table_def['TableName'],
            KeySchema=table_def['KeySchema'],
            AttributeDefinitions=table_def['AttributeDefinitions'],
            BillingMode='PAY_PER_REQUEST'  # Use on-demand billing for local dev
        )
        
        # Wait for table to be created
        print(f"Waiting for table {table_name} to be ready...")
        table.wait_until_exists()
        return True
        
    except Exception as e:
        print(f"❌ Error creating table '{table_name}': {e}")
        return False

if __name__ == "__main__":
    setup_local_tables()