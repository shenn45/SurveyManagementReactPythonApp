import graphene
from graphene import ObjectType, List, Field, String, Int, Boolean, Float, DateTime
from typing import Optional
from datetime import datetime
import uuid
import crud

# Survey List Response Type (matches frontend expectation)
class SurveyType(ObjectType):
    SurveyId = String()
    SurveyNumber = String()
    CustomerId = String()
    PropertyId = String()
    SurveyTypeId = String()
    StatusId = String()
    Title = String()
    Description = String()
    PurposeCode = String()
    RequestDate = DateTime()
    ScheduledDate = DateTime()
    CompletedDate = DateTime()
    DeliveryDate = DateTime()
    DueDate = DateTime()
    QuotedPrice = Float()
    FinalPrice = Float()
    EstimatedCost = Float()
    ActualCost = Float()
    Notes = String()
    IsFieldworkComplete = Boolean()
    IsDrawingComplete = Boolean()
    IsScanned = Boolean()
    IsDelivered = Boolean()
    IsActive = Boolean()
    CreatedDate = DateTime()
    ModifiedDate = DateTime()
    CreatedBy = String()
    ModifiedBy = String()

class SurveyListResponse(ObjectType):
    surveys = List(SurveyType)
    total = Int()
    page = Int()
    size = Int()

class SurveyTypeType(ObjectType):
    SurveyTypeId = String()
    SurveyTypeName = String()
    Description = String()
    IsActive = Boolean()

class SurveyStatusType(ObjectType):
    SurveyStatusId = String()
    StatusName = String()
    Description = String()
    IsActive = Boolean()

class CustomerType(ObjectType):
    CustomerId = String()
    CustomerCode = String()
    CompanyName = String()
    ContactFirstName = String()
    ContactLastName = String()
    Email = String()
    Phone = String()
    Fax = String()
    Website = String()
    IsActive = Boolean()
    CreatedDate = DateTime()
    ModifiedDate = DateTime()
    CreatedBy = String()
    ModifiedBy = String()

class CustomerListResponse(ObjectType):
    customers = List(CustomerType)
    total = Int()
    page = Int()
    size = Int()

class PropertyType(ObjectType):
    PropertyId = String()  # Changed from Int to String to match UUID
    PropertyCode = String()
    PropertyName = String()
    PropertyDescription = String()
    OwnerName = String()
    OwnerPhone = String()
    OwnerEmail = String()
    AddressId = String()  # Changed from Int to String for consistency
    TownshipId = String()  # Changed from Int to String for consistency
    # Frontend expected fields
    SurveyPrimaryKey = Int()  # Keep as Int since it's actually a number
    LegacyTax = String()
    District = String()
    Section = String()
    Block = String()
    Lot = String()
    PropertyType = String()
    IsActive = Boolean()
    CreatedDate = DateTime()
    ModifiedDate = DateTime()
    CreatedBy = String()
    ModifiedBy = String()

class PropertyListResponse(ObjectType):
    properties = List(PropertyType)
    total = Int()
    page = Int()
    size = Int()

class TownshipType(ObjectType):
    TownshipId = String()
    TownshipName = String()
    County = String()
    State = String()
    IsActive = Boolean()
    CreatedDate = DateTime()
    ModifiedDate = DateTime()
    CreatedBy = String()
    ModifiedBy = String()

class TownshipListResponse(ObjectType):
    townships = List(TownshipType)
    total = Int()
    page = Int()
    size = Int()

def model_to_survey(survey):
    """Convert Survey model to GraphQL type"""
    if not survey:
        return None
    
    # Handle both dict (from DynamoDB) and model objects
    if isinstance(survey, dict):
        survey_data = survey
    else:
        survey_data = survey.dict() if hasattr(survey, 'dict') else survey.__dict__
    
    # Helper function to convert price fields (Decimal to float for GraphQL)
    def convert_price_field(field_name):
        value = survey_data.get(field_name)
        if value is None:
            return None
        # Handle Decimal objects from the model
        if hasattr(value, '__float__'):  # This includes Decimal
            return float(value)
        # Handle string or numeric values
        try:
            return float(value) if value != '' else None
        except (ValueError, TypeError):
            return None
    
    # Helper function to convert date fields
    def convert_date_field(field_name):
        value = survey_data.get(field_name)
        if value is None or value == '' or value == 'None':
            return None
        if isinstance(value, str):
            try:
                # Try to parse the date string
                from datetime import datetime
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return None
        return value
    
    return SurveyType(
        SurveyId=str(survey_data.get('SurveyId', '')),
        SurveyNumber=str(survey_data.get('SurveyNumber', '')),
        CustomerId=str(survey_data.get('CustomerId', '')),
        PropertyId=str(survey_data.get('PropertyId', '')),
        SurveyTypeId=str(survey_data.get('SurveyTypeId', '')),
        StatusId=str(survey_data.get('StatusId', survey_data.get('SurveyStatusId', ''))),  # Handle both field names
        Title=str(survey_data.get('Title', '')),
        Description=str(survey_data.get('Description', '')),
        PurposeCode=str(survey_data.get('PurposeCode', '')),
        RequestDate=convert_date_field('RequestDate'),
        ScheduledDate=convert_date_field('ScheduledDate'),
        CompletedDate=convert_date_field('CompletedDate'),
        DeliveryDate=convert_date_field('DeliveryDate'),
        DueDate=convert_date_field('DueDate'),
        QuotedPrice=convert_price_field('QuotedPrice'),
        FinalPrice=convert_price_field('FinalPrice'),
        EstimatedCost=convert_price_field('EstimatedCost'),
        ActualCost=convert_price_field('ActualCost'),
        Notes=str(survey_data.get('Notes', '')),
        IsFieldworkComplete=bool(survey_data.get('IsFieldworkComplete', False)),
        IsDrawingComplete=bool(survey_data.get('IsDrawingComplete', False)),
        IsScanned=bool(survey_data.get('IsScanned', False)),
        IsDelivered=getattr(survey, 'IsDelivered', None),
        IsActive=getattr(survey, 'IsActive', True),
        CreatedDate=convert_date_field('CreatedDate'),
        ModifiedDate=convert_date_field('ModifiedDate'),
        CreatedBy=getattr(survey, 'CreatedBy', None),
        ModifiedBy=getattr(survey, 'ModifiedBy', None)
    )

def model_to_customer(customer):
    """Convert Customer model to GraphQL type"""
    if not customer:
        return None
    return CustomerType(
        CustomerId=customer.CustomerId,
        CustomerCode=getattr(customer, 'CustomerCode', None),
        CompanyName=getattr(customer, 'CompanyName', None),
        ContactFirstName=getattr(customer, 'ContactFirstName', None),
        ContactLastName=getattr(customer, 'ContactLastName', None),
        Email=getattr(customer, 'Email', None),
        Phone=getattr(customer, 'Phone', None),
        Fax=getattr(customer, 'Fax', None),
        Website=getattr(customer, 'Website', None),
        IsActive=getattr(customer, 'IsActive', True),
        CreatedDate=getattr(customer, 'CreatedDate', None),
        ModifiedDate=getattr(customer, 'ModifiedDate', None),
        CreatedBy=getattr(customer, 'CreatedBy', None),
        ModifiedBy=getattr(customer, 'ModifiedBy', None)
    )

def model_to_property(property):
    """Convert Property model to GraphQL type with type conversions for frontend."""
    if not property:
        return None
    
    # Helper function to safely convert to int
    def safe_int(value, default=0):
        try:
            if value is None or value == '':
                return default
            return int(value)
        except (ValueError, TypeError):
            return default
    
    return PropertyType(
        PropertyId=str(getattr(property, 'PropertyId', '')),  # Keep as string
        PropertyCode=getattr(property, 'PropertyCode', None),
        PropertyName=getattr(property, 'PropertyName', None),
        PropertyDescription=getattr(property, 'PropertyDescription', None),
        OwnerName=getattr(property, 'OwnerName', None),
        OwnerPhone=getattr(property, 'OwnerPhone', None),
        OwnerEmail=getattr(property, 'OwnerEmail', None),
        AddressId=str(getattr(property, 'AddressId', '')),  # Keep as string
        TownshipId=str(getattr(property, 'TownshipId', '')),  # Keep as string
        # Frontend expected fields with proper type conversion
        SurveyPrimaryKey=safe_int(getattr(property, 'SurveyPrimaryKey', None)),
        LegacyTax=getattr(property, 'LegacyTax', None),
        District=getattr(property, 'District', None),
        Section=getattr(property, 'Section', None),
        Block=getattr(property, 'Block', None),
        Lot=getattr(property, 'Lot', None),
        PropertyType=getattr(property, 'PropertyType', "Residential"),
        IsActive=getattr(property, 'IsActive', True),
        CreatedDate=getattr(property, 'CreatedDate', None),
        ModifiedDate=getattr(property, 'ModifiedDate', None),
        CreatedBy=getattr(property, 'CreatedBy', None),
        ModifiedBy=getattr(property, 'ModifiedBy', None)
    )

def model_to_township(township):
    """Convert Township model to GraphQL type"""
    if not township:
        return None
    return TownshipType(
        TownshipId=getattr(township, 'TownshipId', ''),
        TownshipName=getattr(township, 'TownshipName', ''),
        County=getattr(township, 'County', ''),
        State=getattr(township, 'State', ''),
        IsActive=getattr(township, 'IsActive', True),
        CreatedDate=getattr(township, 'CreatedDate', None),
        ModifiedDate=getattr(township, 'ModifiedDate', None),
        CreatedBy=getattr(township, 'CreatedBy', ''),
        ModifiedBy=getattr(township, 'ModifiedBy', '')
    )

def model_to_survey_type(survey_type):
    """Convert SurveyType model to GraphQL type"""
    if not survey_type:
        return None
    return SurveyTypeType(
        SurveyTypeId=getattr(survey_type, 'SurveyTypeId', ''),
        SurveyTypeName=getattr(survey_type, 'SurveyTypeName', ''),
        Description=getattr(survey_type, 'Description', ''),
        IsActive=getattr(survey_type, 'IsActive', True)
    )

def model_to_survey_status(survey_status):
    """Convert SurveyStatus model to GraphQL type"""
    if not survey_status:
        return None
    return SurveyStatusType(
        SurveyStatusId=getattr(survey_status, 'SurveyStatusId', ''),
        StatusName=getattr(survey_status, 'StatusName', ''),
        Description=getattr(survey_status, 'Description', ''),
        IsActive=getattr(survey_status, 'IsActive', True)
    )

class Query(ObjectType):
    surveys = Field(SurveyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    survey = Field(SurveyType, surveyId=String(required=True))
    customers = Field(CustomerListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    customer = Field(CustomerType, customerId=String(required=True))
    properties = Field(PropertyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    property = Field(PropertyType, propertyId=String(required=True))
    townships = Field(TownshipListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    township = Field(TownshipType, townshipId=String(required=True))
    surveyTypes = Field(List(SurveyTypeType))
    surveyStatuses = Field(List(SurveyStatusType))

    def resolve_surveys(self, info, skip=0, limit=100, search=None):
        try:
            surveys_data, total = crud.get_surveys(skip=skip, limit=limit, search=search)
            surveys = [model_to_survey(s) for s in surveys_data]
            return SurveyListResponse(
                surveys=surveys,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        except Exception as e:
            print(f"Error resolving surveys: {e}")
            return SurveyListResponse(surveys=[], total=0, page=1, size=limit)

    def resolve_survey(self, info, surveyId):
        try:
            survey_data = crud.get_survey(survey_id=surveyId)
            return model_to_survey(survey_data)
        except Exception as e:
            print(f"Error resolving survey: {e}")
            return None

    def resolve_customers(self, info, skip=0, limit=100, search=None):
        try:
            customers_data, total = crud.get_customers(skip=skip, limit=limit, search=search)
            customers = [model_to_customer(c) for c in customers_data]
            return CustomerListResponse(
                customers=customers,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        except Exception as e:
            print(f"Error resolving customers: {e}")
            return CustomerListResponse(customers=[], total=0, page=1, size=limit)

    def resolve_customer(self, info, customerId):
        try:
            customer_data = crud.get_customer(customer_id=customerId)
            return model_to_customer(customer_data)
        except Exception as e:
            print(f"Error resolving customer: {e}")
            return None

    def resolve_properties(self, info, skip=0, limit=100, search=None):
        try:
            properties_data, total = crud.get_properties(skip=skip, limit=limit, search=search)
            properties = [model_to_property(p) for p in properties_data]
            return PropertyListResponse(
                properties=properties,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        except Exception as e:
            print(f"Error resolving properties: {e}")
            return PropertyListResponse(properties=[], total=0, page=1, size=limit)

    def resolve_property(self, info, propertyId):
        try:
            property_data = crud.get_property(property_id=propertyId)
            return model_to_property(property_data)
        except Exception as e:
            print(f"Error resolving property: {e}")
            return None

    def resolve_townships(self, info, skip=0, limit=100, search=None):
        try:
            townships_data, total = crud.get_townships(skip=skip, limit=limit, search=search)
            townships = [model_to_township(t) for t in townships_data]
            return TownshipListResponse(
                townships=townships,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        except Exception as e:
            print(f"Error resolving townships: {e}")
            return TownshipListResponse(townships=[], total=0, page=1, size=limit)

    def resolve_township(self, info, townshipId):
        try:
            township_data = crud.get_township(township_id=townshipId)
            return model_to_township(township_data)
        except Exception as e:
            print(f"Error resolving township: {e}")
            return None

    def resolve_surveyTypes(self, info):
        try:
            survey_types = crud.get_survey_types()
            return [model_to_survey_type(st) for st in survey_types]
        except Exception as e:
            print(f"Error resolving survey types: {e}")
            return []

    def resolve_surveyStatuses(self, info):
        try:
            survey_statuses = crud.get_survey_statuses()
            return [model_to_survey_status(ss) for ss in survey_statuses]
        except Exception as e:
            print(f"Error resolving survey statuses: {e}")
            return []

# Create simple schema with queries and mutations
class CreateCustomerInput(graphene.InputObjectType):
    CustomerCode = String()
    CompanyName = String(required=True)
    ContactFirstName = String()
    ContactLastName = String()
    Email = String()
    Phone = String()
    Fax = String()
    Website = String()
    IsActive = Boolean()

class CustomerUpdateInput(graphene.InputObjectType):
    CustomerCode = String()
    CompanyName = String()
    ContactFirstName = String()
    ContactLastName = String()
    Email = String()
    Phone = String()
    Fax = String()
    Website = String()
    IsActive = Boolean()

class PropertyInput(graphene.InputObjectType):
    PropertyCode = String(required=True)
    PropertyName = String(required=True) 
    PropertyDescription = String()
    OwnerName = String()
    OwnerPhone = String()
    OwnerEmail = String()
    AddressId = String()
    TownshipId = String()
    IsActive = Boolean()
    # Legacy fields for backward compatibility
    SurveyPrimaryKey = Int()
    LegacyTax = String()
    District = String()
    Section = String()
    Block = String()
    Lot = String()
    PropertyType = String()
    # Extended property fields
    ParcelNumber = String()
    LegalDescription = String()
    Address = String()
    City = String()
    State = String()
    ZipCode = String()
    County = String()
    Acreage = Float()
    SqFootage = Float()
    YearBuilt = Int()
    AssessedValue = Float()
    MarketValue = Float()
    PropertyTaxes = Float()
    Zoning = String()
    LandUse = String()
    Utilities = String()
    AccessRights = String()
    Restrictions = String()
    Easements = String()
    FloodZone = String()
    SoilType = String()
    Topography = String()
    EnvironmentalConcerns = String()
    PreviousSurveys = String()
    Notes = String()
    Section = String()
    Block = String()
    Lot = String()
    PropertyType = String()

class TownshipInput(graphene.InputObjectType):
    TownshipName = String(required=True)
    County = String(required=True)
    State = String(required=True)
    IsActive = Boolean()

class TownshipUpdateInput(graphene.InputObjectType):
    TownshipName = String()
    County = String()
    State = String()
    IsActive = Boolean()

class PropertyUpdateInput(graphene.InputObjectType):
    PropertyCode = String()
    PropertyName = String()
    PropertyDescription = String()
    OwnerName = String()
    OwnerPhone = String()
    OwnerEmail = String()
    AddressId = String()
    TownshipId = String()
    IsActive = Boolean()
    # Legacy fields for backward compatibility
    SurveyPrimaryKey = Int()
    LegacyTax = String()
    District = String()
    Section = String()
    Block = String()
    Lot = String()
    PropertyType = String()
    # Extended property fields
    ParcelNumber = String()
    LegalDescription = String()
    Address = String()
    City = String()
    State = String()
    ZipCode = String()
    County = String()
    Acreage = Float()
    SqFootage = Float()
    YearBuilt = Int()
    AssessedValue = Float()
    MarketValue = Float()
    PropertyTaxes = Float()
    Zoning = String()
    LandUse = String()
    Utilities = String()
    AccessRights = String()
    Restrictions = String()
    Easements = String()
    FloodZone = String()
    SoilType = String()
    Topography = String()
    EnvironmentalConcerns = String()
    PreviousSurveys = String()
    Notes = String()

class CreateSurveyTypeInput(graphene.InputObjectType):
    SurveyTypeName = String(required=True)
    Description = String()
    IsActive = Boolean()

class CreateSurveyStatusInput(graphene.InputObjectType):
    StatusName = String(required=True)
    Description = String()
    IsActive = Boolean()

class SurveyInput(graphene.InputObjectType):
    SurveyNumber = String(required=True)
    CustomerId = String()
    PropertyId = String()
    SurveyTypeId = String()
    StatusId = String()
    Title = String()
    Description = String()
    PurposeCode = String()
    RequestDate = String()
    ScheduledDate = String()
    CompletedDate = String()
    DeliveryDate = String()
    DueDate = String()
    QuotedPrice = Float()
    FinalPrice = Float()
    IsFieldworkComplete = Boolean()
    IsDrawingComplete = Boolean()
    IsScanned = Boolean()
    IsDelivered = Boolean()

class SurveyUpdateInput(graphene.InputObjectType):
    SurveyNumber = String()
    CustomerId = String()
    PropertyId = String()
    SurveyTypeId = String()
    StatusId = String()
    Title = String()
    Description = String()
    PurposeCode = String()
    RequestDate = String()
    ScheduledDate = String()
    CompletedDate = String()
    DeliveryDate = String()
    DueDate = String()
    QuotedPrice = Float()
    FinalPrice = Float()
    EstimatedCost = Float()
    ActualCost = Float()
    Notes = String()
    IsFieldworkComplete = Boolean()
    IsDrawingComplete = Boolean()
    IsScanned = Boolean()
    IsDelivered = Boolean()
    IsActive = Boolean()

class CreateCustomerMutation(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)
    
    customer = Field(CustomerType)
    
    def mutate(self, info, input):
        try:
            from schemas import CustomerCreate
            customer_data = CustomerCreate(**input)
            customer = crud.create_customer(customer=customer_data)
            return CreateCustomerMutation(customer=model_to_customer(customer))
        except Exception as e:
            print(f"Error creating customer: {e}")
            return CreateCustomerMutation(customer=None)

class UpdateCustomerMutation(graphene.Mutation):
    class Arguments:
        customer_id = String(required=True)
        input = CustomerUpdateInput(required=True)
    
    customer = Field(CustomerType)
    
    def mutate(self, info, customer_id, input):
        try:
            from schemas import CustomerUpdate
            customer_data = CustomerUpdate(**input)
            customer = crud.update_customer(customer_id=customer_id, customer=customer_data)
            return UpdateCustomerMutation(customer=model_to_customer(customer))
        except Exception as e:
            print(f"Error updating customer: {e}")
            return UpdateCustomerMutation(customer=None)

class DeleteCustomerMutation(graphene.Mutation):
    class Arguments:
        customer_id = String(required=True)
    
    success = Boolean()
    
    def mutate(self, info, customer_id):
        try:
            crud.delete_customer(customer_id=customer_id)
            return DeleteCustomerMutation(success=True)
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return DeleteCustomerMutation(success=False)

class CreatePropertyMutation(graphene.Mutation):
    class Arguments:
        input = PropertyInput(required=True)
    
    property = Field(PropertyType)
    
    def mutate(self, info, input):
        try:
            from schemas import PropertyCreate
            # Create PropertyCreate schema object for CRUD
            property_data = PropertyCreate(**input)
            property = crud.create_property(property=property_data)
            if property:
                return CreatePropertyMutation(property=model_to_property(property))
            return None
        except Exception as e:
            print(f"Error creating property: {e}")
            import traceback
            traceback.print_exc()
            return None
            return None

class UpdatePropertyMutation(graphene.Mutation):
    class Arguments:
        propertyId = String(required=True)
        input = PropertyUpdateInput(required=True)
    
    property = Field(PropertyType)
    
    def mutate(self, info, propertyId, input):
        try:
            from schemas import PropertyUpdate
            # Create PropertyUpdate schema object for CRUD
            property_data = PropertyUpdate(**input)
            property = crud.update_property(property_id=propertyId, property=property_data)
            if property:
                return UpdatePropertyMutation(property=model_to_property(property))
            return None
        except Exception as e:
            print(f"Error updating property: {e}")
            import traceback
            traceback.print_exc()
            return None

class CreateTownshipMutation(graphene.Mutation):
    class Arguments:
        input = TownshipInput(required=True)
    
    township = Field(TownshipType)
    
    def mutate(self, info, input):
        try:
            from schemas import TownshipCreate
            township_data = TownshipCreate(**input)
            township = crud.create_township(township=township_data)
            return CreateTownshipMutation(township=model_to_township(township))
        except Exception as e:
            print(f"Error creating township: {e}")
            return CreateTownshipMutation(township=None)

class UpdateTownshipMutation(graphene.Mutation):
    class Arguments:
        townshipId = String(required=True)
        input = TownshipUpdateInput(required=True)
    
    township = Field(TownshipType)
    
    def mutate(self, info, townshipId, input):
        try:
            from schemas import TownshipUpdate
            township_data = TownshipUpdate(**input)
            township = crud.update_township(township_id=townshipId, township=township_data)
            return UpdateTownshipMutation(township=model_to_township(township))
        except Exception as e:
            print(f"Error updating township: {e}")
            return UpdateTownshipMutation(township=None)

class DeleteTownshipMutation(graphene.Mutation):
    class Arguments:
        townshipId = String(required=True)
    
    success = Boolean()
    
    def mutate(self, info, townshipId):
        try:
            success = crud.delete_township(township_id=townshipId)
            return DeleteTownshipMutation(success=success)
        except Exception as e:
            print(f"Error deleting township: {e}")
            return DeleteTownshipMutation(success=False)

class DeletePropertyMutation(graphene.Mutation):
    class Arguments:
        propertyId = String(required=True)
    
    success = Boolean()
    
    def mutate(self, info, propertyId):
        try:
            success = crud.delete_property(property_id=propertyId)
            return DeletePropertyMutation(success=success)
        except Exception as e:
            print(f"Error deleting property: {e}")
            return DeletePropertyMutation(success=False)

class CreateSurveyTypeMutation(graphene.Mutation):
    class Arguments:
        input = CreateSurveyTypeInput(required=True)
    
    surveyType = Field(SurveyTypeType)
    
    def mutate(self, info, input):
        try:
            from models import SurveyType
            # Convert GraphQL input to dictionary
            input_dict = {
                'SurveyTypeName': input.SurveyTypeName,
                'Description': input.Description,
                'IsActive': input.IsActive if input.IsActive is not None else True
            }
            survey_type_data = SurveyType(**input_dict)
            survey_type = crud.create_survey_type(survey_type_data)
            return CreateSurveyTypeMutation(surveyType=model_to_survey_type(survey_type))
        except Exception as e:
            print(f"Error creating survey type: {e}")
            return CreateSurveyTypeMutation(surveyType=None)

class CreateSurveyStatusMutation(graphene.Mutation):
    class Arguments:
        input = CreateSurveyStatusInput(required=True)
    
    surveyStatus = Field(SurveyStatusType)
    
    def mutate(self, info, input):
        try:
            from models import SurveyStatus
            # Convert GraphQL input to dictionary
            input_dict = {
                'StatusName': input.StatusName,
                'Description': input.Description,
                'IsActive': input.IsActive if input.IsActive is not None else True
            }
            survey_status_data = SurveyStatus(**input_dict)
            survey_status = crud.create_survey_status(survey_status_data)
            return CreateSurveyStatusMutation(surveyStatus=model_to_survey_status(survey_status))
        except Exception as e:
            print(f"Error creating survey status: {e}")
            return CreateSurveyStatusMutation(surveyStatus=None)

class CreateSurveyMutation(graphene.Mutation):
    class Arguments:
        input = SurveyInput(required=True)
    
    survey = Field(SurveyType)
    
    def mutate(self, info, input):
        try:
            # Use the models.Survey directly instead of schemas.SurveyCreate
            from models import Survey
            
            print(f"Received input: {input}")
            print(f"Input type: {type(input)}")
            
            # Convert GraphQL input to dictionary with proper field mapping
            # Handle required fields with defaults if not provided
            input_dict = {
                'SurveyId': str(uuid.uuid4()),  # Generate new UUID
                'SurveyNumber': str(input.SurveyNumber) if input.SurveyNumber else f"SURVEY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                'CustomerId': str(input.CustomerId) if input.CustomerId else str(uuid.uuid4()),  # Convert to string and provide default
                'PropertyId': str(input.PropertyId) if input.PropertyId else str(uuid.uuid4()),  # Convert to string and provide default
                'SurveyTypeId': str(input.SurveyTypeId) if input.SurveyTypeId else str(uuid.uuid4()),  # Convert to string and provide default
                'StatusId': str(input.StatusId) if input.StatusId else str(uuid.uuid4()),  # Keep as StatusId (not SurveyStatusId) to match DynamoDB structure
            }
            
            # Add optional fields if provided
            if hasattr(input, 'Title') and input.Title:
                input_dict['Title'] = str(input.Title)
            if hasattr(input, 'Description') and input.Description:
                input_dict['Description'] = str(input.Description)
            if hasattr(input, 'PurposeCode') and input.PurposeCode:
                input_dict['PurposeCode'] = str(input.PurposeCode)
            if hasattr(input, 'RequestDate') and input.RequestDate:
                input_dict['RequestDate'] = str(input.RequestDate)
            if hasattr(input, 'ScheduledDate') and input.ScheduledDate:
                input_dict['ScheduledDate'] = str(input.ScheduledDate)
            if hasattr(input, 'CompletedDate') and input.CompletedDate:
                input_dict['CompletedDate'] = str(input.CompletedDate)
            if hasattr(input, 'DeliveryDate') and input.DeliveryDate:
                input_dict['DeliveryDate'] = str(input.DeliveryDate)
            if hasattr(input, 'DueDate') and input.DueDate:
                input_dict['DueDate'] = str(input.DueDate)
            if hasattr(input, 'QuotedPrice') and input.QuotedPrice:
                from decimal import Decimal
                input_dict['QuotedPrice'] = Decimal(str(input.QuotedPrice))
            if hasattr(input, 'FinalPrice') and input.FinalPrice:
                from decimal import Decimal
                input_dict['FinalPrice'] = Decimal(str(input.FinalPrice))
            if hasattr(input, 'IsFieldworkComplete') and input.IsFieldworkComplete is not None:
                input_dict['IsFieldworkComplete'] = bool(input.IsFieldworkComplete)
            if hasattr(input, 'IsDrawingComplete') and input.IsDrawingComplete is not None:
                input_dict['IsDrawingComplete'] = bool(input.IsDrawingComplete)
            if hasattr(input, 'IsScanned') and input.IsScanned is not None:
                input_dict['IsScanned'] = bool(input.IsScanned)
                
            print(f"Creating survey with data: {input_dict}")
                
            # Save directly to DynamoDB without using the Survey model
            from database import get_table
            from crud import serialize_item
            
            table = get_table('Surveys')
            if table is None:
                print("Error: Could not get Surveys table")
                return CreateSurveyMutation(survey=None)
            
            # Convert data to the format expected by DynamoDB
            survey_data = {
                'SurveyId': input_dict['SurveyId'],
                'SurveyNumber': input_dict['SurveyNumber'],
                'SurveyTypeId': input_dict['SurveyTypeId'],
                'CustomerId': input_dict['CustomerId'],
                'PropertyId': input_dict['PropertyId'],
                'StatusId': input_dict['StatusId'],  # Keep as StatusId
                'CreatedDate': datetime.now().isoformat(),
                'ModifiedDate': datetime.now().isoformat(),
                'IsActive': True,
            }
            
            # Add optional fields if provided
            if hasattr(input, 'Title') and input.Title:
                survey_data['Title'] = str(input.Title)
            if hasattr(input, 'Description') and input.Description:
                survey_data['Description'] = str(input.Description)
            if hasattr(input, 'PurposeCode') and input.PurposeCode:
                survey_data['PurposeCode'] = str(input.PurposeCode)
            if hasattr(input, 'RequestDate') and input.RequestDate:
                survey_data['RequestDate'] = str(input.RequestDate)
            if hasattr(input, 'ScheduledDate') and input.ScheduledDate:
                survey_data['ScheduledDate'] = str(input.ScheduledDate)
            if hasattr(input, 'CompletedDate') and input.CompletedDate:
                survey_data['CompletedDate'] = str(input.CompletedDate)
            if hasattr(input, 'DeliveryDate') and input.DeliveryDate:
                survey_data['DeliveryDate'] = str(input.DeliveryDate)
            if hasattr(input, 'DueDate') and input.DueDate:
                survey_data['DueDate'] = str(input.DueDate)
            if hasattr(input, 'QuotedPrice') and input.QuotedPrice:
                from decimal import Decimal
                survey_data['QuotedPrice'] = Decimal(str(input.QuotedPrice))
            if hasattr(input, 'FinalPrice') and input.FinalPrice:
                from decimal import Decimal
                survey_data['FinalPrice'] = Decimal(str(input.FinalPrice))
            if hasattr(input, 'IsFieldworkComplete') and input.IsFieldworkComplete is not None:
                survey_data['IsFieldworkComplete'] = bool(input.IsFieldworkComplete)
            if hasattr(input, 'IsDrawingComplete') and input.IsDrawingComplete is not None:
                survey_data['IsDrawingComplete'] = bool(input.IsDrawingComplete)
            if hasattr(input, 'IsScanned') and input.IsScanned is not None:
                survey_data['IsScanned'] = bool(input.IsScanned)
            
            serialized_data = serialize_item(survey_data)
            
            print(f"Saving to DynamoDB: {serialized_data}")
            table.put_item(Item=serialized_data)
            
            print(f"Survey created successfully: {survey_data['SurveyId']}")
            
            return CreateSurveyMutation(survey=model_to_survey(survey_data))
            
        except Exception as e:
            print(f"Error creating survey: {e}")
            import traceback
            traceback.print_exc()
            import traceback
            traceback.print_exc()
            return CreateSurveyMutation(survey=None)

class UpdateSurveyMutation(graphene.Mutation):
    class Arguments:
        surveyId = String(required=True)
        input = SurveyUpdateInput(required=True)
    
    survey = Field(SurveyType)
    
    def mutate(self, info, surveyId, input):
        try:
            from schemas import SurveyUpdate
            
            print(f"Updating survey {surveyId} with input: {input}")
            
            # Convert GraphQL input to schema object
            # Only include non-None values to allow partial updates
            input_dict = {}
            
            # Helper function to add field if it exists and is not None or empty string
            def add_field(field_name, value=None, is_date_field=False):
                if value is None:
                    value = getattr(input, field_name, None)
                if value is not None:
                    # Skip empty strings for date fields
                    if is_date_field and value == '':
                        return
                    # Skip empty strings for string fields too (optional)
                    if isinstance(value, str) and value == '' and field_name in ['Description', 'PurposeCode']:
                        return
                    input_dict[field_name] = value
            
            # Add all possible fields
            add_field('SurveyNumber')
            add_field('CustomerId')
            add_field('PropertyId')
            add_field('SurveyTypeId')
            add_field('StatusId')
            add_field('Title')
            add_field('Description')
            add_field('PurposeCode')
            add_field('RequestDate', is_date_field=True)
            add_field('ScheduledDate', is_date_field=True)
            add_field('CompletedDate', is_date_field=True)
            add_field('DeliveryDate', is_date_field=True)
            add_field('DueDate', is_date_field=True)
            add_field('QuotedPrice')
            add_field('FinalPrice')
            add_field('EstimatedCost')
            add_field('ActualCost')
            add_field('Notes')
            add_field('IsFieldworkComplete')
            add_field('IsDrawingComplete')
            add_field('IsScanned')
            add_field('IsDelivered')
            add_field('IsActive')
            
            print(f"Creating SurveyUpdate with data: {input_dict}")
            print(f"Types in input_dict: {[(k, type(v)) for k, v in input_dict.items()]}")
            
            # Convert all numeric fields to Decimal before creating schema object
            from decimal import Decimal
            decimal_fields = ['QuotedPrice', 'FinalPrice', 'EstimatedCost', 'ActualCost']
            for field in decimal_fields:
                if field in input_dict and isinstance(input_dict[field], (int, float)):
                    old_value = input_dict[field]
                    input_dict[field] = Decimal(str(old_value))
                    print(f"Converted {field} from {type(old_value)} {old_value} to {type(input_dict[field])} {input_dict[field]}")
            
            print(f"Final input_dict types: {[(k, type(v)) for k, v in input_dict.items()]}")
            
            # Debug: Print all values with their types
            print("About to create SurveyUpdate with:")
            for k, v in input_dict.items():
                print(f"  {k}: {v} (type: {type(v)})")
            
            # Create SurveyUpdate schema object
            try:
                survey_data = SurveyUpdate(**input_dict)
                print("SurveyUpdate created successfully")
            except Exception as schema_error:
                print(f"Error creating SurveyUpdate schema: {schema_error}")
                raise schema_error
            
            # Call CRUD function
            updated_survey = crud.update_survey(survey_id=surveyId, survey=survey_data)
            
            if updated_survey:
                print(f"Survey updated successfully: {surveyId}")
                return UpdateSurveyMutation(survey=model_to_survey(updated_survey))
            else:
                print(f"Failed to update survey: {surveyId}")
                return UpdateSurveyMutation(survey=None)
                
        except Exception as e:
            print(f"Error updating survey: {e}")
            import traceback
            traceback.print_exc()
            return UpdateSurveyMutation(survey=None)

class Mutation(graphene.ObjectType):
    createCustomer = CreateCustomerMutation.Field()
    updateCustomer = UpdateCustomerMutation.Field()
    deleteCustomer = DeleteCustomerMutation.Field()
    createProperty = CreatePropertyMutation.Field()
    updateProperty = UpdatePropertyMutation.Field()
    deleteProperty = DeletePropertyMutation.Field()
    create_township = CreateTownshipMutation.Field()
    update_township = UpdateTownshipMutation.Field()
    delete_township = DeleteTownshipMutation.Field()
    createSurvey = CreateSurveyMutation.Field()
    updateSurvey = UpdateSurveyMutation.Field()
    createSurveyType = CreateSurveyTypeMutation.Field()
    createSurveyStatus = CreateSurveyStatusMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)