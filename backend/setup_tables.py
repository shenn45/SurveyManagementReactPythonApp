#!/usr/bin/env python3
"""
Unified DynamoDB table setup script for local development
Combines functionality from setup_tables.py and setup_additional_tables.py
"""
import sys
import os
import boto3

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import DYNAMODB_TABLES

def connect_to_dynamodb():
    """Connect to local DynamoDB instance"""
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8001',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
            region_name='us-east-1'
        )
        
        # Test connection by listing existing tables
        existing_tables = list(dynamodb.tables.all())
        print(f"✓ Connected to local DynamoDB at http://localhost:8001")
        print(f"  Existing tables: {[table.name for table in existing_tables]}")
        
        return dynamodb, [table.name for table in existing_tables]
        
    except Exception as e:
        print(f"✗ Error connecting to DynamoDB: {e}")
        print("  Make sure moto server is running: python -m moto.server -p 8001 -H 0.0.0.0")
        return None, []

def create_table_from_model(dynamodb, table_name):
    """Create a DynamoDB table using the definition from models.py"""
    
    if table_name not in DYNAMODB_TABLES:
        print(f"❌ No table definition found for '{table_name}'")
        return False
    
    table_def = DYNAMODB_TABLES[table_name]
    
    try:
        print(f"  Creating table: {table_name}")
        
        # Prepare table creation parameters
        create_params = {
            'TableName': table_def['TableName'],
            'KeySchema': table_def['KeySchema'],
            'AttributeDefinitions': table_def['AttributeDefinitions'],
            'BillingMode': 'PAY_PER_REQUEST'  # Use on-demand billing for local dev
        }
        
        # Add Global Secondary Indexes if they exist
        if 'GlobalSecondaryIndexes' in table_def:
            gsi_list = []
            for gsi in table_def['GlobalSecondaryIndexes']:
                gsi_config = {
                    'IndexName': gsi['IndexName'],
                    'KeySchema': gsi['KeySchema'],
                    'Projection': {'ProjectionType': 'ALL'}  # Project all attributes for local dev
                }
                gsi_list.append(gsi_config)
                
                # Add any additional attribute definitions needed for GSI
                if 'AttributeDefinitions' in gsi:
                    for attr_def in gsi['AttributeDefinitions']:
                        # Only add if not already in main attribute definitions
                        if attr_def not in create_params['AttributeDefinitions']:
                            create_params['AttributeDefinitions'].append(attr_def)
            
            create_params['GlobalSecondaryIndexes'] = gsi_list
        
        # Create the table
        table = dynamodb.create_table(**create_params)
        
        # Wait for table to be ready
        print(f"  Waiting for table {table_name} to be ready...")
        table.wait_until_exists()
        
        print(f"✓ Table {table_name} created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error creating table '{table_name}': {e}")
        return False

def create_table_simple(dynamodb, table_name, key_attribute, key_type='S'):
    """Create a simple table with just a hash key (fallback method)"""
    try:
        print(f"  Creating simple table: {table_name}")
        
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': key_attribute,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': key_attribute,
                    'AttributeType': key_type
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        print(f"  Waiting for table {table_name} to be ready...")
        table.wait_until_exists()
        
        print(f"✓ Simple table {table_name} created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error creating simple table '{table_name}': {e}")
        return False

def setup_all_tables():
    """Setup all required DynamoDB tables for the application"""
    
    print("🚀 Starting DynamoDB table setup...")
    print("=" * 50)
    
    # Connect to DynamoDB
    dynamodb, existing_tables = connect_to_dynamodb()
    if not dynamodb:
        return False
    
    # Define all required tables
    all_tables = [
        'Addresses',
        'Customers', 
        'CustomerAddresses',
        'Townships',
        'Properties',
        'SurveyTypes',
        'SurveyStatuses', 
        'Surveys',
        'SurveyFiles',
        'Documents',
        'UserSettings'
    ]
    
    print(f"\n📋 Required tables: {all_tables}")
    print(f"📋 Tables to create: {[t for t in all_tables if t not in existing_tables]}")
    print()
    
    success_count = 0
    total_count = 0
    
    # Create missing tables
    for table_name in all_tables:
        total_count += 1
        
        if table_name in existing_tables:
            print(f"✓ Table {table_name} already exists")
            success_count += 1
            continue
        
        # Try to create table using model definition
        if create_table_from_model(dynamodb, table_name):
            success_count += 1
        else:
            # Fallback to simple table creation for critical tables
            fallback_tables = {
                'Customers': 'CustomerId',
                'Surveys': 'SurveyId', 
                'Properties': 'PropertyId',
                'Townships': 'TownshipId',
                'SurveyTypes': 'SurveyTypeId',
                'SurveyStatuses': 'SurveyStatusId'
            }
            
            if table_name in fallback_tables:
                print(f"  Attempting fallback creation for {table_name}...")
                if create_table_simple(dynamodb, table_name, fallback_tables[table_name]):
                    success_count += 1
    
    print()
    print("=" * 50)
    if success_count == total_count:
        print("✅ All tables are ready!")
        print(f"   Successfully processed {success_count}/{total_count} tables")
        return True
    else:
        print(f"⚠️  Partial success: {success_count}/{total_count} tables ready")
        print("   Some tables may need manual creation")
        return False

def verify_tables():
    """Verify that all tables exist and are accessible"""
    
    print("\n🔍 Verifying table setup...")
    
    dynamodb, existing_tables = connect_to_dynamodb()
    if not dynamodb:
        return False
    
    required_tables = [
        'Customers', 'Surveys', 'Properties', 'Townships',
        'SurveyTypes', 'SurveyStatuses', 'UserSettings'
    ]
    
    missing_tables = [t for t in required_tables if t not in existing_tables]
    
    if not missing_tables:
        print("✅ All core tables verified successfully!")
        return True
    else:
        print(f"❌ Missing core tables: {missing_tables}")
        return False

# Legacy function for backward compatibility
def create_tables():
    """Legacy function that calls the new unified setup"""
    return setup_all_tables()

if __name__ == "__main__":
    print("DynamoDB Table Setup Script")
    print("==========================")
    
    success = setup_all_tables()
    
    if success:
        verify_tables()
        print("\n🎉 Setup completed successfully!")
        print("   You can now run your application.")
    else:
        print("\n❌ Setup completed with errors.")
        print("   Please check the error messages above.")
        sys.exit(1)