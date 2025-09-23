import requests
import json

def create_survey_type(name, description):
    """Create a survey type using GraphQL mutation"""
    url = "http://localhost:8000/graphql"
    
    mutation = f"""
    mutation {{
        createSurveyType(input: {{
            SurveyTypeName: "{name}"
            Description: "{description}"
            IsActive: true
        }}) {{
            surveyType {{
                SurveyTypeId
                SurveyTypeName
                Description
                IsActive
            }}
        }}
    }}
    """
    
    try:
        response = requests.post(url, json={"query": mutation})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def create_survey_status(name, description):
    """Create a survey status using GraphQL mutation"""
    url = "http://localhost:8000/graphql"
    
    mutation = f"""
    mutation {{
        createSurveyStatus(input: {{
            StatusName: "{name}"
            Description: "{description}"
            IsActive: true
        }}) {{
            surveyStatus {{
                SurveyStatusId
                StatusName
                Description
                IsActive
            }}
        }}
    }}
    """
    
    try:
        response = requests.post(url, json={"query": mutation})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Survey Types
survey_types = [
    ("Boundary Survey", "A survey that establishes or reestablishes boundaries of a parcel using its legal description."),
    ("Topographic Survey", "A survey that shows the elevations and contours of the land surface."),
    ("ALTA/NSPS Land Title Survey", "A standardized type of survey that meets specific requirements set by the American Land Title Association and National Society of Professional Surveyors."),
    ("Subdivision Survey", "A survey that divides a tract of land into smaller parcels for development."),
    ("Construction Survey", "A survey that provides precise measurements and locations for construction projects."),
    ("As-Built Survey", "A survey that documents the final constructed locations of buildings and improvements."),
    ("Mortgage Survey", "A simplified boundary survey often required by mortgage lenders."),
    ("Easement Survey", "A survey that identifies and maps easements and rights-of-way."),
    ("Flood Elevation Certificate", "A survey that determines the elevation of a structure in relation to flood zones.")
]

# Survey Statuses
survey_statuses = [
    ("Requested", "Survey has been requested but not yet started."),
    ("In Progress", "Survey work is currently underway."),
    ("Field Work Complete", "Field work has been completed, processing data."),
    ("Draft Complete", "Draft survey has been completed and is under review."),
    ("Client Review", "Survey is with client for review and approval."),
    ("Revisions Required", "Client has requested revisions to the survey."),
    ("Final Review", "Survey is undergoing final internal review."),
    ("Completed", "Survey has been completed and delivered to client."),
    ("On Hold", "Survey work has been temporarily suspended."),
    ("Cancelled", "Survey has been cancelled by client or due to other circumstances.")
]

print("=" * 60)
print("Survey Management Database Seeding (GraphQL)")
print("=" * 60)

print("\nCreating Survey Types...")
types_created = 0
for name, description in survey_types:
    result = create_survey_type(name, description)
    if "data" in result and result["data"] and result["data"]["createSurveyType"]["surveyType"]:
        types_created += 1
        print(f"✓ Created: {name}")
    else:
        print(f"✗ Failed: {name}")
        if "errors" in result:
            print(f"  Error: {result['errors']}")

print(f"\nCreated {types_created}/{len(survey_types)} survey types")

print("\nCreating Survey Statuses...")
statuses_created = 0
for name, description in survey_statuses:
    result = create_survey_status(name, description)
    if "data" in result and result["data"] and result["data"]["createSurveyStatus"]["surveyStatus"]:
        statuses_created += 1
        print(f"✓ Created: {name}")
    else:
        print(f"✗ Failed: {name}")
        if "errors" in result:
            print(f"  Error: {result['errors']}")

print(f"\nCreated {statuses_created}/{len(survey_statuses)} survey statuses")

print("\n" + "=" * 60)
print("Seeding Summary:")
print(f"Survey Types: {types_created}/{len(survey_types)}")
print(f"Survey Statuses: {statuses_created}/{len(survey_statuses)}")
print("=" * 60)