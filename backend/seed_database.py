#!/usr/bin/env python3
"""
Database seeding script for Survey Management App
Seeds the database with mock survey types, survey statuses, and townships
"""

import sys
import os
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import SurveyType, SurveyStatus, Township
import crud

def get_local_dynamodb():
    """Get a direct connection to local moto DynamoDB"""
    return boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8001',
        aws_access_key_id='fake_access_key',
        aws_secret_access_key='fake_secret_key',
        region_name='us-east-1'
    )

def get_survey_types_direct():
    """Get survey types directly from local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('SurveyTypes')
        response = table.scan(
            FilterExpression=Attr('IsActive').eq(True)
        )
        return response.get('Items', [])
    except Exception as e:
        print(f"Error getting survey types: {e}")
        return []

def get_survey_statuses_direct():
    """Get survey statuses directly from local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('SurveyStatuses')
        response = table.scan(
            FilterExpression=Attr('IsActive').eq(True)
        )
        return response.get('Items', [])
    except Exception as e:
        print(f"Error getting survey statuses: {e}")
        return []

def create_survey_type_direct(survey_type_data):
    """Create survey type directly in local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('SurveyTypes')
        
        # Prepare the item
        item = {
            'SurveyTypeId': str(uuid.uuid4()),
            'SurveyTypeName': survey_type_data['SurveyTypeName'],
            'Description': survey_type_data.get('Description', ''),
            'IsActive': True,
            'CreatedDate': datetime.now().isoformat(),
            'ModifiedDate': datetime.now().isoformat()
        }
        
        table.put_item(Item=item)
        return True
    except Exception as e:
        print(f"Error creating survey type: {e}")
        return False

def get_townships_direct():
    """Get townships directly from local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('Townships')
        response = table.scan(
            FilterExpression=Attr('IsActive').eq(True)
        )
        return response.get('Items', [])
    except Exception as e:
        print(f"Error getting townships: {e}")
        return []

def create_township_direct(township_data):
    """Create township directly in local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('Townships')
        
        # Prepare the item
        item = {
            'TownshipId': str(uuid.uuid4()),
            'TownshipName': township_data['TownshipName'],
            'County': township_data['County'],
            'State': township_data['State'],
            'IsActive': True,
            'CreatedDate': datetime.now().isoformat(),
            'ModifiedDate': datetime.now().isoformat(),
            'CreatedBy': 'system',
            'ModifiedBy': 'system'
        }
        
        table.put_item(Item=item)
        return True
    except Exception as e:
        print(f"Error creating township: {e}")
        return False

def create_survey_status_direct(survey_status_data):
    """Create survey status directly in local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('SurveyStatuses')
        
        # Prepare the item
        item = {
            'SurveyStatusId': str(uuid.uuid4()),
            'StatusName': survey_status_data['StatusName'],
            'Description': survey_status_data.get('Description', ''),
            'IsActive': True,
            'CreatedDate': datetime.now().isoformat(),
            'ModifiedDate': datetime.now().isoformat()
        }
        
        table.put_item(Item=item)
        return True
    except Exception as e:
        print(f"Error creating survey status: {e}")
        return False

def seed_survey_types():
    """Seed the database with common survey types"""
    survey_types = [
        {
            "SurveyTypeName": "Boundary Survey",
            "Description": "A survey that establishes or reestablishes boundaries of a parcel using its legal description."
        },
        {
            "SurveyTypeName": "Topographic Survey", 
            "Description": "A survey that shows the elevations and contours of the land surface."
        },
        {
            "SurveyTypeName": "ALTA/NSPS Land Title Survey",
            "Description": "A standardized type of survey that meets specific requirements set by the American Land Title Association and National Society of Professional Surveyors."
        },
        {
            "SurveyTypeName": "Subdivision Survey",
            "Description": "A survey that divides a tract of land into smaller parcels for development."
        },
        {
            "SurveyTypeName": "Construction Survey",
            "Description": "A survey that provides precise measurements and locations for construction projects."
        },
        {
            "SurveyTypeName": "As-Built Survey",
            "Description": "A survey that documents the final constructed locations of buildings and improvements."
        },
        {
            "SurveyTypeName": "Mortgage Survey",
            "Description": "A simplified boundary survey often required by mortgage lenders."
        },
        {
            "SurveyTypeName": "Easement Survey",
            "Description": "A survey that identifies and maps easements and rights-of-way."
        },
        {
            "SurveyTypeName": "Flood Elevation Certificate",
            "Description": "A survey that determines the elevation of a structure in relation to flood zones."
        }
    ]
    
    print("Seeding Survey Types...")
    created_count = 0
    
    for survey_type_data in survey_types:
        result = create_survey_type_direct(survey_type_data)
        
        if result:
            created_count += 1
            print(f"✓ Created survey type: {survey_type_data['SurveyTypeName']}")
        else:
            print(f"✗ Failed to create survey type: {survey_type_data['SurveyTypeName']}")
    
    print(f"Created {created_count} survey types out of {len(survey_types)} total.")
    return created_count

def seed_survey_statuses():
    """Seed the database with common survey statuses"""
    survey_statuses = [
        {
            "StatusName": "Requested",
            "Description": "Survey has been requested but not yet started."
        },
        {
            "StatusName": "In Progress",
            "Description": "Survey work is currently underway."
        },
        {
            "StatusName": "Field Work Complete",
            "Description": "Field work has been completed, processing data."
        },
        {
            "StatusName": "Draft Complete",
            "Description": "Draft survey has been completed and is under review."
        },
        {
            "StatusName": "Client Review",
            "Description": "Survey is with client for review and approval."
        },
        {
            "StatusName": "Revisions Required",
            "Description": "Client has requested revisions to the survey."
        },
        {
            "StatusName": "Final Review",
            "Description": "Survey is undergoing final internal review."
        },
        {
            "StatusName": "Completed",
            "Description": "Survey has been completed and delivered to client."
        },
        {
            "StatusName": "On Hold",
            "Description": "Survey work has been temporarily suspended."
        },
        {
            "StatusName": "Cancelled",
            "Description": "Survey has been cancelled by client or due to other circumstances."
        }
    ]
    
    print("\nSeeding Survey Statuses...")
    created_count = 0
    
    for survey_status_data in survey_statuses:
        result = create_survey_status_direct(survey_status_data)
        
        if result:
            created_count += 1
            print(f"✓ Created survey status: {survey_status_data['StatusName']}")
        else:
            print(f"✗ Failed to create survey status: {survey_status_data['StatusName']}")
    
    print(f"Created {created_count} survey statuses out of {len(survey_statuses)} total.")
    return created_count

def seed_townships():
    """Seed the database with townships from Suffolk County, New York"""
    townships = [
        {
            "TownshipName": "Babylon",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Brookhaven",
            "County": "Suffolk", 
            "State": "New York"
        },
        {
            "TownshipName": "East Hampton",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Huntington",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Islip",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Riverhead",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Shelter Island",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Smith Point",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Southampton",
            "County": "Suffolk",
            "State": "New York"
        },
        {
            "TownshipName": "Southold",
            "County": "Suffolk",
            "State": "New York"
        }
    ]
    
    print("\nSeeding Townships (Suffolk County, NY)...")
    created_count = 0
    
    for township_data in townships:
        result = create_township_direct(township_data)
        
        if result:
            created_count += 1
            print(f"✓ Created township: {township_data['TownshipName']}, {township_data['County']} County, {township_data['State']}")
        else:
            print(f"✗ Failed to create township: {township_data['TownshipName']}")
    
    print(f"Created {created_count} townships out of {len(townships)} total.")
    return created_count

def check_existing_data():
    """Check if there's already data in the tables"""
    existing_types = get_survey_types_direct()
    existing_statuses = get_survey_statuses_direct()
    existing_townships = get_townships_direct()
    
    print(f"Existing survey types: {len(existing_types)}")
    print(f"Existing survey statuses: {len(existing_statuses)}")
    print(f"Existing townships: {len(existing_townships)}")
    
    return len(existing_types), len(existing_statuses), len(existing_townships)

def main():
    """Main seeding function"""
    print("=" * 60)
    print("Survey Management Database Seeding Script")
    print("=" * 60)
    
    try:
        # Check existing data
        type_count, status_count, township_count = check_existing_data()
        
        if type_count > 0 or status_count > 0 or township_count > 0:
            print(f"\nWarning: Found existing data in tables.")
            response = input("Do you want to proceed anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Seeding cancelled.")
                return
        
        # Seed the data
        types_created = seed_survey_types()
        statuses_created = seed_survey_statuses()
        townships_created = seed_townships()
        
        print("\n" + "=" * 60)
        print("Seeding Summary:")
        print(f"Survey Types Created: {types_created}")
        print(f"Survey Statuses Created: {statuses_created}")
        print(f"Townships Created: {townships_created}")
        print("=" * 60)
        
        if types_created > 0 or statuses_created > 0 or townships_created > 0:
            print("✓ Database seeding completed successfully!")
        else:
            print("⚠ No new records were created.")
            
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()