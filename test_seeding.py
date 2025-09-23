import requests
import json

def test_survey_type_creation():
    url = "http://localhost:8000/graphql"
    
    mutation = """
    mutation {
        createSurveyType(input: {
            SurveyTypeName: "Test Boundary Survey"
            Description: "A test survey to establish boundaries"
            IsActive: true
        }) {
            surveyType {
                SurveyTypeId
                SurveyTypeName
                Description
                IsActive
            }
        }
    }
    """
    
    response = requests.post(url, json={"query": mutation})
    result = response.json()
    print("Response Status:", response.status_code)
    print("Full Response:")
    print(json.dumps(result, indent=2))
    
    # Check if there was an error
    if 'errors' in result:
        print("\nGraphQL Errors:")
        for error in result['errors']:
            print(f"- {error}")
    
    # Check the data
    if 'data' in result and result['data']:
        create_result = result['data'].get('createSurveyType')
        if create_result and create_result.get('surveyType'):
            print("\n✓ Survey type created successfully!")
            survey_type = create_result['surveyType']
            print(f"ID: {survey_type.get('SurveyTypeId')}")
            print(f"Name: {survey_type.get('SurveyTypeName')}")
            print(f"Description: {survey_type.get('Description')}")
        else:
            print("\n✗ Survey type creation returned null")
    else:
        print("\n✗ No data returned")

if __name__ == "__main__":
    test_survey_type_creation()