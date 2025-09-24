#!/usr/bin/env python3
"""
Mock data seeding script for Survey Management App
Seeds the database with mock customers, properties, and surveys
"""

import sys
import os
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Customer, Property, Survey
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

def get_existing_data():
    """Get existing data from tables"""
    try:
        dynamodb = get_local_dynamodb()
        
        # Get survey types
        survey_types_table = dynamodb.Table('SurveyTypes')
        survey_types_response = survey_types_table.scan(FilterExpression=Attr('IsActive').eq(True))
        survey_types = survey_types_response.get('Items', [])
        
        # Get survey statuses
        survey_statuses_table = dynamodb.Table('SurveyStatuses')
        survey_statuses_response = survey_statuses_table.scan(FilterExpression=Attr('IsActive').eq(True))
        survey_statuses = survey_statuses_response.get('Items', [])
        
        # Get townships
        townships_table = dynamodb.Table('Townships')
        townships_response = townships_table.scan(FilterExpression=Attr('IsActive').eq(True))
        townships = townships_response.get('Items', [])
        
        return survey_types, survey_statuses, townships
    except Exception as e:
        print(f"Error getting existing data: {e}")
        return [], [], []

def create_customer_direct(customer_data):
    """Create customer directly in local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('Customers')
        
        # Prepare the item
        item = {
            'CustomerId': str(uuid.uuid4()),
            'CustomerCode': customer_data.get('CustomerCode', ''),
            'CompanyName': customer_data['CompanyName'],
            'ContactFirstName': customer_data.get('ContactFirstName', ''),
            'ContactLastName': customer_data.get('ContactLastName', ''),
            'Email': customer_data.get('Email', ''),
            'Phone': customer_data.get('Phone', ''),
            'Fax': customer_data.get('Fax', ''),
            'Website': customer_data.get('Website', ''),
            'IsActive': True,
            'CreatedDate': datetime.now().isoformat(),
            'ModifiedDate': datetime.now().isoformat(),
            'CreatedBy': 'system',
            'ModifiedBy': 'system'
        }
        
        table.put_item(Item=item)
        return item
    except Exception as e:
        print(f"Error creating customer: {e}")
        return None

def create_property_direct(property_data):
    """Create property directly in local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('Properties')
        
        # Prepare the item
        item = {
            'PropertyId': str(uuid.uuid4()),
            'PropertyCode': property_data['PropertyCode'],
            'PropertyName': property_data['PropertyName'],
            'PropertyDescription': property_data.get('PropertyDescription', ''),
            'OwnerName': property_data.get('OwnerName', ''),
            'OwnerPhone': property_data.get('OwnerPhone', ''),
            'OwnerEmail': property_data.get('OwnerEmail', ''),
            'TownshipId': property_data.get('TownshipId', ''),
            'SurveyPrimaryKey': property_data.get('SurveyPrimaryKey', 0),
            'LegacyTax': property_data.get('LegacyTax', ''),
            'District': property_data.get('District', ''),
            'Section': property_data.get('Section', ''),
            'Block': property_data.get('Block', ''),
            'Lot': property_data.get('Lot', ''),
            'PropertyType': property_data.get('PropertyType', 'Residential'),
            'Address': property_data.get('Address', ''),
            'City': property_data.get('City', ''),
            'State': property_data.get('State', 'New York'),
            'ZipCode': property_data.get('ZipCode', ''),
            'County': property_data.get('County', 'Suffolk'),
            'IsActive': True,
            'CreatedDate': datetime.now().isoformat(),
            'ModifiedDate': datetime.now().isoformat(),
            'CreatedBy': 'system',
            'ModifiedBy': 'system'
        }
        
        table.put_item(Item=item)
        return item
    except Exception as e:
        print(f"Error creating property: {e}")
        return None

def create_survey_direct(survey_data):
    """Create survey directly in local DynamoDB"""
    try:
        dynamodb = get_local_dynamodb()
        table = dynamodb.Table('Surveys')
        
        # Prepare the item
        item = {
            'SurveyId': str(uuid.uuid4()),
            'SurveyNumber': survey_data['SurveyNumber'],
            'CustomerId': survey_data['CustomerId'],
            'PropertyId': survey_data['PropertyId'],
            'SurveyTypeId': survey_data['SurveyTypeId'],
            'StatusId': survey_data['StatusId'],
            'Title': survey_data.get('Title', ''),
            'Description': survey_data.get('Description', ''),
            'PurposeCode': survey_data.get('PurposeCode', ''),
            'RequestDate': survey_data.get('RequestDate', ''),
            'ScheduledDate': survey_data.get('ScheduledDate', ''),
            'CompletedDate': survey_data.get('CompletedDate', ''),
            'DeliveryDate': survey_data.get('DeliveryDate', ''),
            'DueDate': survey_data.get('DueDate', ''),
            'QuotedPrice': survey_data.get('QuotedPrice', Decimal('0')),
            'FinalPrice': survey_data.get('FinalPrice', Decimal('0')),
            'EstimatedCost': survey_data.get('EstimatedCost', Decimal('0')),
            'ActualCost': survey_data.get('ActualCost', Decimal('0')),
            'Notes': survey_data.get('Notes', ''),
            'IsFieldworkComplete': survey_data.get('IsFieldworkComplete', False),
            'IsDrawingComplete': survey_data.get('IsDrawingComplete', False),
            'IsScanned': survey_data.get('IsScanned', False),
            'IsDelivered': survey_data.get('IsDelivered', False),
            'IsActive': True,
            'CreatedDate': datetime.now().isoformat(),
            'ModifiedDate': datetime.now().isoformat(),
            'CreatedBy': 'system',
            'ModifiedBy': 'system'
        }
        
        table.put_item(Item=item)
        return item
    except Exception as e:
        print(f"Error creating survey: {e}")
        return None

def seed_customers():
    """Seed the database with mock customers"""
    customers = [
        {
            "CustomerCode": "ACME001",
            "CompanyName": "ACME Development Corporation",
            "ContactFirstName": "John",
            "ContactLastName": "Smith",
            "Email": "j.smith@acmedev.com",
            "Phone": "(631) 555-0101",
            "Website": "www.acmedev.com"
        },
        {
            "CustomerCode": "SUFF002",
            "CompanyName": "Suffolk County Engineering",
            "ContactFirstName": "Maria",
            "ContactLastName": "Rodriguez",
            "Email": "m.rodriguez@suffolk.gov",
            "Phone": "(631) 555-0202"
        },
        {
            "CustomerCode": "HAMP003",
            "CompanyName": "Hamptons Real Estate Group",
            "ContactFirstName": "Robert",
            "ContactLastName": "Johnson",
            "Email": "robert@hamptonsrealestate.com",
            "Phone": "(631) 555-0303",
            "Website": "www.hamptonsrealestate.com"
        },
        {
            "CustomerCode": "LONG004",
            "CompanyName": "Long Island Construction Co.",
            "ContactFirstName": "Sarah",
            "ContactLastName": "Davis",
            "Email": "sarah.davis@liconst.com",
            "Phone": "(631) 555-0404",
            "Fax": "(631) 555-0405"
        },
        {
            "CustomerCode": "EAST005",
            "CompanyName": "East End Properties LLC",
            "ContactFirstName": "Michael",
            "ContactLastName": "Wilson",
            "Email": "m.wilson@eastendprops.com",
            "Phone": "(631) 555-0505"
        },
        {
            "CustomerCode": "HUNT006",
            "CompanyName": "Huntington Bay Developers",
            "ContactFirstName": "Jennifer",
            "ContactLastName": "Brown",
            "Email": "jen.brown@huntingtonbay.com",
            "Phone": "(631) 555-0606",
            "Website": "www.huntingtonbay.com"
        },
        {
            "CustomerCode": "BAYL007",
            "CompanyName": "Bayfront Land Trust",
            "ContactFirstName": "David",
            "ContactLastName": "Miller",
            "Email": "dmiller@bayfronttrust.org",
            "Phone": "(631) 555-0707"
        },
        {
            "CustomerCode": "ISLP008",
            "CompanyName": "Islip Town Planning Department",
            "ContactFirstName": "Lisa",
            "ContactLastName": "Anderson",
            "Email": "l.anderson@isliptown.gov",
            "Phone": "(631) 555-0808"
        }
    ]
    
    print("Seeding Customers...")
    created_customers = []
    created_count = 0
    
    for customer_data in customers:
        customer = create_customer_direct(customer_data)
        if customer:
            created_customers.append(customer)
            created_count += 1
            print(f"✓ Created customer: {customer_data['CompanyName']}")
        else:
            print(f"✗ Failed to create customer: {customer_data['CompanyName']}")
    
    print(f"Created {created_count} customers out of {len(customers)} total.")
    return created_customers

def seed_properties(townships):
    """Seed the database with mock properties"""
    if not townships:
        print("No townships found - cannot create properties without township references")
        return []
    
    # Property data with Suffolk County addresses
    properties_data = [
        {
            "PropertyCode": "PROP001",
            "PropertyName": "Oceanfront Parcel - Montauk",
            "PropertyDescription": "Prime oceanfront development parcel with 300 feet of beach frontage",
            "OwnerName": "Coastal Holdings LLC",
            "OwnerPhone": "(631) 555-1001",
            "OwnerEmail": "info@coastalholdings.com",
            "Address": "123 Montauk Highway",
            "City": "Montauk",
            "ZipCode": "11954",
            "District": "001",
            "Section": "12",
            "Block": "A",
            "Lot": "15",
            "PropertyType": "Commercial"
        },
        {
            "PropertyCode": "PROP002", 
            "PropertyName": "Residential Lot - Bay Shore",
            "PropertyDescription": "Single family residential building lot in established neighborhood",
            "OwnerName": "John and Mary Peterson",
            "OwnerPhone": "(631) 555-1002",
            "Address": "456 Maple Street",
            "City": "Bay Shore",
            "ZipCode": "11706",
            "District": "002",
            "Section": "08",
            "Block": "B",
            "Lot": "23",
            "PropertyType": "Residential"
        },
        {
            "PropertyCode": "PROP003",
            "PropertyName": "Industrial Complex - Ronkonkoma",
            "PropertyDescription": "Light industrial facility with warehouse and office space",
            "OwnerName": "Suffolk Industrial Partners",
            "OwnerPhone": "(631) 555-1003",
            "Address": "789 Industrial Boulevard",
            "City": "Ronkonkoma", 
            "ZipCode": "11779",
            "District": "003",
            "Section": "15",
            "Block": "C",
            "Lot": "07",
            "PropertyType": "Industrial"
        },
        {
            "PropertyCode": "PROP004",
            "PropertyName": "Historic Estate - Sag Harbor",
            "PropertyDescription": "Historic waterfront estate with original 1890s mansion",
            "OwnerName": "Heritage Preservation Society",
            "OwnerPhone": "(631) 555-1004",
            "Address": "321 Harbor View Road",
            "City": "Sag Harbor",
            "ZipCode": "11963",
            "District": "004",
            "Section": "22",
            "Block": "D",
            "Lot": "01",
            "PropertyType": "Historic"
        },
        {
            "PropertyCode": "PROP005",
            "PropertyName": "Shopping Center - Commack",
            "PropertyDescription": "Regional shopping center with anchor stores and parking",
            "OwnerName": "Retail Development Corp",
            "OwnerPhone": "(631) 555-1005",
            "Address": "654 Veteran's Highway",
            "City": "Commack",
            "ZipCode": "11725",
            "District": "005",
            "Section": "18",
            "Block": "E",
            "Lot": "12",
            "PropertyType": "Commercial"
        },
        {
            "PropertyCode": "PROP006",
            "PropertyName": "Agricultural Land - Riverhead",
            "PropertyDescription": "Working farm with 50 acres of cultivated land",
            "OwnerName": "Green Fields Farm LLC",
            "OwnerPhone": "(631) 555-1006",
            "Address": "987 Sound Avenue",
            "City": "Riverhead",
            "ZipCode": "11901",
            "District": "006",
            "Section": "25",
            "Block": "F",
            "Lot": "05",
            "PropertyType": "Agricultural"
        },
        {
            "PropertyCode": "PROP007",
            "PropertyName": "Waterfront Condo Site - Huntington",
            "PropertyDescription": "Approved condominium development site with harbor views",
            "OwnerName": "Harbor Point Developers",
            "OwnerPhone": "(631) 555-1007",
            "Address": "147 Harbor Road",
            "City": "Huntington",
            "ZipCode": "11743",
            "District": "007",
            "Section": "11",
            "Block": "G",
            "Lot": "18",
            "PropertyType": "Residential"
        },
        {
            "PropertyCode": "PROP008",
            "PropertyName": "Office Complex - Melville",
            "PropertyDescription": "Class A office building with professional tenants",
            "OwnerName": "Corporate Center Holdings",
            "OwnerPhone": "(631) 555-1008",
            "Address": "258 Broad Hollow Road",
            "City": "Melville",
            "ZipCode": "11747",
            "District": "008",
            "Section": "14",
            "Block": "H",
            "Lot": "09",
            "PropertyType": "Commercial"
        }
    ]
    
    print("\nSeeding Properties...")
    created_properties = []
    created_count = 0
    
    for prop_data in properties_data:
        # Assign random township
        township = random.choice(townships)
        prop_data['TownshipId'] = township['TownshipId']
        prop_data['SurveyPrimaryKey'] = random.randint(1000, 9999)
        prop_data['LegacyTax'] = f"S{random.randint(100000, 999999)}"
        
        property_item = create_property_direct(prop_data)
        if property_item:
            created_properties.append(property_item)
            created_count += 1
            print(f"✓ Created property: {prop_data['PropertyName']}")
        else:
            print(f"✗ Failed to create property: {prop_data['PropertyName']}")
    
    print(f"Created {created_count} properties out of {len(properties_data)} total.")
    return created_properties

def seed_surveys(customers, properties, survey_types, survey_statuses):
    """Seed the database with mock surveys"""
    if not all([customers, properties, survey_types, survey_statuses]):
        print("Missing required data - cannot create surveys without customers, properties, survey types, and statuses")
        return []
    
    print("\nSeeding Surveys...")
    created_surveys = []
    created_count = 0
    
    # Create 15 mock surveys with various statuses and dates
    survey_count = 15
    
    for i in range(survey_count):
        # Random selections
        customer = random.choice(customers)
        property_item = random.choice(properties)
        survey_type = random.choice(survey_types)
        survey_status = random.choice(survey_statuses)
        
        # Generate dates
        request_date = datetime.now() - timedelta(days=random.randint(30, 365))
        scheduled_date = request_date + timedelta(days=random.randint(5, 30))
        due_date = scheduled_date + timedelta(days=random.randint(10, 60))
        
        # Determine completion based on status
        is_completed = survey_status['StatusName'] in ['Completed', 'Final Review']
        completed_date = scheduled_date + timedelta(days=random.randint(1, 30)) if is_completed else None
        delivery_date = completed_date + timedelta(days=random.randint(1, 7)) if completed_date else None
        
        # Generate prices
        base_price = random.randint(2500, 15000)
        quoted_price = Decimal(str(base_price))
        final_price = Decimal(str(base_price + random.randint(-500, 1000))) if is_completed else Decimal('0')
        
        survey_data = {
            "SurveyNumber": f"SURV-2024-{(i+1):03d}",
            "CustomerId": customer['CustomerId'],
            "PropertyId": property_item['PropertyId'],
            "SurveyTypeId": survey_type['SurveyTypeId'],
            "StatusId": survey_status['SurveyStatusId'],
            "Title": f"{survey_type['SurveyTypeName']} - {property_item['PropertyName']}",
            "Description": f"Professional {survey_type['SurveyTypeName'].lower()} for {property_item['PropertyName']} in {property_item['City']}",
            "PurposeCode": random.choice(['DEV', 'REF', 'LEG', 'TIT', 'CON']),
            "RequestDate": request_date.isoformat(),
            "ScheduledDate": scheduled_date.isoformat(),
            "DueDate": due_date.isoformat(),
            "CompletedDate": completed_date.isoformat() if completed_date else '',
            "DeliveryDate": delivery_date.isoformat() if delivery_date else '',
            "QuotedPrice": quoted_price,
            "FinalPrice": final_price,
            "EstimatedCost": Decimal(str(int(quoted_price * Decimal('0.7')))),
            "ActualCost": Decimal(str(int(final_price * Decimal('0.8')))) if final_price > 0 else Decimal('0'),
            "Notes": f"Survey requested by {customer['CompanyName']} for property development project.",
            "IsFieldworkComplete": is_completed,
            "IsDrawingComplete": is_completed,
            "IsScanned": is_completed,
            "IsDelivered": survey_status['StatusName'] == 'Completed'
        }
        
        survey = create_survey_direct(survey_data)
        if survey:
            created_surveys.append(survey)
            created_count += 1
            print(f"✓ Created survey: {survey_data['SurveyNumber']} - {survey_data['Title'][:50]}...")
        else:
            print(f"✗ Failed to create survey: {survey_data['SurveyNumber']}")
    
    print(f"Created {created_count} surveys out of {survey_count} total.")
    return created_surveys

def check_existing_data():
    """Check if there's already data in the tables"""
    try:
        dynamodb = get_local_dynamodb()
        
        customers_table = dynamodb.Table('Customers')
        customers_response = customers_table.scan()
        customer_count = len(customers_response.get('Items', []))
        
        properties_table = dynamodb.Table('Properties')
        properties_response = properties_table.scan()
        property_count = len(properties_response.get('Items', []))
        
        surveys_table = dynamodb.Table('Surveys')
        surveys_response = surveys_table.scan()
        survey_count = len(surveys_response.get('Items', []))
        
        print(f"Existing customers: {customer_count}")
        print(f"Existing properties: {property_count}")
        print(f"Existing surveys: {survey_count}")
        
        return customer_count, property_count, survey_count
    except Exception as e:
        print(f"Error checking existing data: {e}")
        return 0, 0, 0

def main():
    """Main seeding function"""
    print("=" * 70)
    print("Survey Management Mock Data Seeding Script")
    print("=" * 70)
    
    try:
        # Check existing data
        customer_count, property_count, survey_count = check_existing_data()
        
        if customer_count > 0 or property_count > 0 or survey_count > 0:
            print(f"\nWarning: Found existing data in tables.")
            response = input("Do you want to proceed anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Seeding cancelled.")
                return
        
        # Get required reference data
        print("\nGetting reference data (survey types, statuses, townships)...")
        survey_types, survey_statuses, townships = get_existing_data()
        
        if not survey_types:
            print("⚠ No survey types found. Please run seed_database.py first to create survey types and statuses.")
            return
        
        if not survey_statuses:
            print("⚠ No survey statuses found. Please run seed_database.py first to create survey statuses.")
            return
            
        if not townships:
            print("⚠ No townships found. Please run seed_database.py first to create townships.")
            return
        
        print(f"Found {len(survey_types)} survey types, {len(survey_statuses)} statuses, {len(townships)} townships")
        
        # Seed the data
        created_customers = seed_customers()
        created_properties = seed_properties(townships)
        created_surveys = seed_surveys(created_customers, created_properties, survey_types, survey_statuses)
        
        print("\n" + "=" * 70)
        print("Mock Data Seeding Summary:")
        print(f"Customers Created: {len(created_customers)}")
        print(f"Properties Created: {len(created_properties)}")
        print(f"Surveys Created: {len(created_surveys)}")
        print("=" * 70)
        
        if created_customers or created_properties or created_surveys:
            print("✓ Mock data seeding completed successfully!")
        else:
            print("⚠ No new records were created.")
            
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()