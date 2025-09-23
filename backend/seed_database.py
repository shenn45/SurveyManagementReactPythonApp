#!/usr/bin/env python3
"""
Database seeding script for Survey Management App
Seeds the database with mock survey types and survey statuses
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import SurveyType, SurveyStatus
import crud

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
        survey_type = SurveyType(**survey_type_data)
        result = crud.create_survey_type(survey_type)
        
        if result:
            created_count += 1
            print(f"✓ Created survey type: {survey_type.SurveyTypeName}")
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
        survey_status = SurveyStatus(**survey_status_data)
        result = crud.create_survey_status(survey_status)
        
        if result:
            created_count += 1
            print(f"✓ Created survey status: {survey_status.StatusName}")
        else:
            print(f"✗ Failed to create survey status: {survey_status_data['StatusName']}")
    
    print(f"Created {created_count} survey statuses out of {len(survey_statuses)} total.")
    return created_count

def check_existing_data():
    """Check if there's already data in the tables"""
    existing_types = crud.get_survey_types()
    existing_statuses = crud.get_survey_statuses()
    
    print(f"Existing survey types: {len(existing_types)}")
    print(f"Existing survey statuses: {len(existing_statuses)}")
    
    return len(existing_types), len(existing_statuses)

def main():
    """Main seeding function"""
    print("=" * 60)
    print("Survey Management Database Seeding Script")
    print("=" * 60)
    
    try:
        # Check existing data
        type_count, status_count = check_existing_data()
        
        if type_count > 0 or status_count > 0:
            print(f"\nWarning: Found existing data in tables.")
            response = input("Do you want to proceed anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Seeding cancelled.")
                return
        
        # Seed the data
        types_created = seed_survey_types()
        statuses_created = seed_survey_statuses()
        
        print("\n" + "=" * 60)
        print("Seeding Summary:")
        print(f"Survey Types Created: {types_created}")
        print(f"Survey Statuses Created: {statuses_created}")
        print("=" * 60)
        
        if types_created > 0 or statuses_created > 0:
            print("✓ Database seeding completed successfully!")
        else:
            print("⚠ No new records were created.")
            
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()