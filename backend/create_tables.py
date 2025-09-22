#!/usr/bin/env python3""""""

"""

Create DynamoDB tables for local developmentDynamoDB Table Creation ScriptDynamoDB Table Creation Script

"""

import boto3Creates all the required DynamoDB tables for the Survey Management applicationCreates all the required DynamoDB tables for the Survey Management application

from dotenv import load_dotenv

import os""""""



load_dotenv()



def create_tables():import boto3import boto3

    """Create the required DynamoDB tables"""

    dynamodb = boto3.resource(import osimport os

        'dynamodb',

        endpoint_url='http://localhost:8001',from dotenv import load_dotenvfrom dotenv import load_dotenv

        aws_access_key_id='fake_access_key',

        aws_secret_access_key='fake_secret_key',

        region_name='us-east-1'

    )load_dotenv()load_dotenv()

    

    tables_to_create = [

        {

            'name': 'Customers',def create_dynamodb_tables():def create_dynamodb_tables():

            'key': 'CustomerId'

        },    """Create all DynamoDB tables for the Survey Management application"""    """Create all DynamoDB tables for the Survey Management application"""

        {

            'name': 'Surveys',         

            'key': 'SurveyId'

        },    # DynamoDB configuration    # DynamoDB configuration

        {

            'name': 'Properties',    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

            'key': 'PropertyId'

        }    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "fake_access_key")    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "fake_access_key")

    ]

        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "fake_secret_key")    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "fake_secret_key")

    for table_config in tables_to_create:

        try:    DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8001")    DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8001")

            table = dynamodb.create_table(

                TableName=table_config['name'],        

                KeySchema=[

                    {    session = boto3.Session(    session = boto3.Session(

                        'AttributeName': table_config['key'],

                        'KeyType': 'HASH'        aws_access_key_id=AWS_ACCESS_KEY_ID,        aws_access_key_id=AWS_ACCESS_KEY_ID,

                    }

                ],        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,

                AttributeDefinitions=[

                    {        region_name=AWS_REGION        region_name=AWS_REGION

                        'AttributeName': table_config['key'],

                        'AttributeType': 'S'    )    )

                    }

                ],        

                BillingMode='PAY_PER_REQUEST'

            )    if DYNAMODB_ENDPOINT_URL:    if DYNAMODB_ENDPOINT_URL:

            

            print(f"✅ Created {table_config['name']} table")        # For local development (DynamoDB Local)        # For local development (DynamoDB Local)

            

            # Wait for table to be created        dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)        dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)

            table.wait_until_exists()

                    print(f"Using local DynamoDB endpoint: {DYNAMODB_ENDPOINT_URL}")        print(f"Using local DynamoDB endpoint: {DYNAMODB_ENDPOINT_URL}")

        except Exception as e:

            if "ResourceInUseException" in str(e):    else:    else:

                print(f"✅ {table_config['name']} table already exists")

            else:        # For AWS DynamoDB        # For AWS DynamoDB

                print(f"❌ Error creating {table_config['name']} table: {e}")

        dynamodb = session.resource('dynamodb')        dynamodb = session.resource('dynamodb')

if __name__ == "__main__":

    print("Creating DynamoDB tables...")        print(f"Using AWS DynamoDB in region: {AWS_REGION}")        print(f"Using AWS DynamoDB in region: {AWS_REGION}")

    create_tables()

    print("Done!")        

    # Define tables to create    # Define tables to create

    tables_to_create = [    tables_to_create = [

        {        {

            'name': 'Customers',            'name': 'Customers',

            'key': 'CustomerId'            'key': 'CustomerId'

        },        },

        {        {

            'name': 'Surveys',             'name': 'Surveys', 

            'key': 'SurveyId'            'key': 'SurveyId'

        },        },

        {        {

            'name': 'Properties',            'name': 'Properties',

            'key': 'PropertyId'            'key': 'PropertyId'

        }        }

    ]    ]

        

    # Create each table    # Create each table

    for table_config in tables_to_create:    for table_config in tables_to_create:

        try:        try:

            print(f"Creating table: {table_config['name']}")            print(f"Creating table: {table_config['name']}")

                        

            table = dynamodb.create_table(            table = dynamodb.create_table(

                TableName=table_config['name'],                TableName=table_config['name'],

                KeySchema=[                KeySchema=[

                    {                    {

                        'AttributeName': table_config['key'],                        'AttributeName': table_config['key'],

                        'KeyType': 'HASH'                        'KeyType': 'HASH'

                    }                    }

                ],                ],

                AttributeDefinitions=[                AttributeDefinitions=[

                    {                    {

                        'AttributeName': table_config['key'],                        'AttributeName': table_config['key'],

                        'AttributeType': 'S'                        'AttributeType': 'S'

                    }                    }

                ],                ],

                BillingMode='PAY_PER_REQUEST'                BillingMode='PAY_PER_REQUEST'

            )            )

                        

            print(f"✅ Created {table_config['name']} table")            print(f"✅ Created {table_config['name']} table")

                        

            # Wait for table to be created            # Wait for table to be created

            table.wait_until_exists()            table.wait_until_exists()

                        

        except Exception as e:        except Exception as e:

            if "ResourceInUseException" in str(e):            if "ResourceInUseException" in str(e):

                print(f"✅ {table_config['name']} table already exists")                print(f"✅ {table_config['name']} table already exists")

            else:            else:

                print(f"❌ Error creating {table_config['name']} table: {e}")                print(f"❌ Error creating {table_config['name']} table: {e}")



if __name__ == "__main__":if __name__ == "__main__":

    print("Creating DynamoDB tables...")    print("Creating DynamoDB tables...")

    create_dynamodb_tables()    create_dynamodb_tables()

    print("Done!")    print("Done!")
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