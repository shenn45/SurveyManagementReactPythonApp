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
DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")  # For local development

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
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        if DYNAMODB_ENDPOINT_URL:
            # For local development (DynamoDB Local)
            self._dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
        else:
            # For AWS DynamoDB
            self._dynamodb = session.resource('dynamodb')
    
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
    return dynamodb.Table(table_name)
