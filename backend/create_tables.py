"""
DynamoDB Table Creation Script
Creates all the required DynamoDB tables for the Survey Management application
"""

import boto3
import os
from dotenv import load_dotenv
from models import DYNAMODB_TABLES

load_dotenv()

def create_dynamodb_tables():
    """Create all DynamoDB tables for the Survey Management application"""
    
    # DynamoDB configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")  # For local development
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    if DYNAMODB_ENDPOINT_URL:
        # For local development (DynamoDB Local)
        dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
        print(f"Using local DynamoDB endpoint: {DYNAMODB_ENDPOINT_URL}")
    else:
        # For AWS DynamoDB
        dynamodb = session.resource('dynamodb')
        print(f"Using AWS DynamoDB in region: {AWS_REGION}")
    
    # Create each table
    for table_name, table_config in DYNAMODB_TABLES.items():
        try:
            print(f"Creating table: {table_name}")
            
            # Prepare table creation parameters
            create_params = {
                'TableName': table_config['TableName'],
                'KeySchema': table_config['KeySchema'],
                'AttributeDefinitions': table_config['AttributeDefinitions'],
                'BillingMode': 'PAY_PER_REQUEST'  # On-demand billing
            }
            
            # Add Global Secondary Indexes if they exist
            if 'GlobalSecondaryIndexes' in table_config:
                gsi_config = []
                for gsi in table_config['GlobalSecondaryIndexes']:
                    gsi_item = {
                        'IndexName': gsi['IndexName'],
                        'KeySchema': gsi['KeySchema'],
                        'Projection': {'ProjectionType': 'ALL'}
                    }
                    gsi_config.append(gsi_item)
                    
                    # Add any missing attribute definitions for GSI
                    for attr in gsi.get('AttributeDefinitions', []):
                        if attr not in create_params['AttributeDefinitions']:
                            create_params['AttributeDefinitions'].append(attr)
                
                create_params['GlobalSecondaryIndexes'] = gsi_config
            
            # Create the table
            table = dynamodb.create_table(**create_params)
            
            # Wait for table to be created
            print(f"Waiting for table {table_name} to be created...")
            table.wait_until_exists()
            
            print(f"✓ Table {table_name} created successfully")
            
        except dynamodb.meta.client.exceptions.ResourceInUseException:
            print(f"⚠ Table {table_name} already exists, skipping...")
        except Exception as e:
            print(f"✗ Error creating table {table_name}: {str(e)}")

def delete_all_tables():
    """Delete all DynamoDB tables (use with caution!)"""
    
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    if DYNAMODB_ENDPOINT_URL:
        dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
    else:
        dynamodb = session.resource('dynamodb')
    
    for table_name in DYNAMODB_TABLES.keys():
        try:
            table = dynamodb.Table(table_name)
            table.delete()
            print(f"✓ Table {table_name} deleted")
        except Exception as e:
            print(f"✗ Error deleting table {table_name}: {str(e)}")

def list_tables():
    """List all existing DynamoDB tables"""
    
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    if DYNAMODB_ENDPOINT_URL:
        dynamodb = session.client('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
    else:
        dynamodb = session.client('dynamodb')
    
    try:
        response = dynamodb.list_tables()
        tables = response.get('TableNames', [])
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
    except Exception as e:
        print(f"Error listing tables: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "create":
            print("Creating DynamoDB tables...")
            create_dynamodb_tables()
            print("Table creation complete!")
            
        elif command == "delete":
            confirm = input("Are you sure you want to delete ALL tables? (yes/no): ")
            if confirm.lower() == "yes":
                print("Deleting all tables...")
                delete_all_tables()
                print("Table deletion complete!")
            else:
                print("Operation cancelled.")
                
        elif command == "list":
            list_tables()
            
        else:
            print("Unknown command. Use: create, delete, or list")
    else:
        print("Usage: python create_tables.py [create|delete|list]")
        print("  create - Create all DynamoDB tables")
        print("  delete - Delete all DynamoDB tables")
        print("  list   - List existing tables")