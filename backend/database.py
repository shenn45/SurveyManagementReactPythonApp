import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# DynamoDB configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT", os.getenv("DYNAMODB_ENDPOINT_URL"))  # For local development

class DynamoDBConnection:
    _instance = None
    _dynamodb = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DynamoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._dynamodb is None:
            self._initialize_connection()
    
    def _initialize_connection(self):
        try:
            # Use environment variables or defaults for local development
            access_key = AWS_ACCESS_KEY_ID or "fake_access_key"
            secret_key = AWS_SECRET_ACCESS_KEY or "fake_secret_key"
            
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=AWS_REGION
            )
            
            if DYNAMODB_ENDPOINT_URL:
                # Try to connect to local DynamoDB
                self._dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
                print(f"Attempting to connect to local DynamoDB at {DYNAMODB_ENDPOINT_URL}")
                
                # Test the connection by trying to list tables
                try:
                    list(self._dynamodb.tables.all())
                    print("Successfully connected to local DynamoDB")
                except Exception as conn_error:
                    print(f"Failed to connect to local DynamoDB: {conn_error}")
                    print("Using development mode with mock data instead")
                    self._dynamodb = None
            else:
                # Use AWS DynamoDB
                self._dynamodb = session.resource('dynamodb')
                print("Connecting to AWS DynamoDB")
                
        except Exception as e:
            print(f"Warning: Could not connect to DynamoDB: {e}")
            print("Using development mode with mock data")
            self._dynamodb = None
    
    @property
    def dynamodb(self):
        return self._dynamodb

# Global instance
db_connection = DynamoDBConnection()

def get_dynamodb():
    """Get DynamoDB connection"""
    return db_connection.dynamodb

def get_table(table_name: str):
    """Get a specific DynamoDB table"""
    dynamodb = get_dynamodb()
    if dynamodb is None:
        print(f"Warning: DynamoDB not available, using mock data for table {table_name}")
        return None
    return dynamodb.Table(table_name)
