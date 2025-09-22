#!/usr/bin/env python3
"""
Start a local DynamoDB server using moto for development
"""
import os
import sys
from moto import mock_dynamodb
from moto.server import run_simple
import boto3
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    """Create the required DynamoDB tables"""
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8001',
        aws_access_key_id='fake_access_key',
        aws_secret_access_key='fake_secret_key',
        region_name='us-east-1'
    )
    
    # Create Customers table
    try:
        customers_table = dynamodb.create_table(
            TableName='Customers',
            KeySchema=[
                {
                    'AttributeName': 'CustomerId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'CustomerId',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Created Customers table")
    except Exception as e:
        print(f"Customers table might already exist: {e}")
    
    # Create Surveys table
    try:
        surveys_table = dynamodb.create_table(
            TableName='Surveys',
            KeySchema=[
                {
                    'AttributeName': 'SurveyId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'SurveyId',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Created Surveys table")
    except Exception as e:
        print(f"Surveys table might already exist: {e}")
    
    # Create Properties table
    try:
        properties_table = dynamodb.create_table(
            TableName='Properties',
            KeySchema=[
                {
                    'AttributeName': 'PropertyId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PropertyId',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Created Properties table")
    except Exception as e:
        print(f"Properties table might already exist: {e}")

if __name__ == "__main__":
    print("Starting local DynamoDB server on port 8001...")
    print("You can create tables by running: python create_tables.py")
    
    # Start the moto DynamoDB server
    try:
        run_simple(
            "localhost", 
            8001, 
            None,  # Will be set up by moto
            threaded=True,
            use_reloader=False,
            use_debugger=False
        )
    except KeyboardInterrupt:
        print("\nShutting down DynamoDB server...")
        sys.exit(0)