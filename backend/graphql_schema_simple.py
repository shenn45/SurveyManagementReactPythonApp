import graphene
from graphene import ObjectType, List, Field, String, Int, Boolean, Float, DateTime
from typing import Optional
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
    PropertyId = Int()  # Frontend expects number
    PropertyCode = String()
    PropertyName = String()
    PropertyDescription = String()
    OwnerName = String()
    OwnerPhone = String()
    OwnerEmail = String()
    AddressId = Int()  # Frontend expects number
    TownshipId = Int()  # Frontend expects number
    # Frontend expected fields
    SurveyPrimaryKey = Int()  # Frontend expects number
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
    return SurveyType(
        SurveyId=survey.SurveyId,
        SurveyNumber=getattr(survey, 'SurveyNumber', None),
        CustomerId=getattr(survey, 'CustomerId', None),
        PropertyId=getattr(survey, 'PropertyId', None),
        SurveyTypeId=getattr(survey, 'SurveyTypeId', None),
        StatusId=getattr(survey, 'StatusId', None),
        Title=getattr(survey, 'Title', None),
        Description=getattr(survey, 'Description', None),
        PurposeCode=getattr(survey, 'PurposeCode', None),
        RequestDate=getattr(survey, 'RequestDate', None),
        ScheduledDate=getattr(survey, 'ScheduledDate', None),
        CompletedDate=getattr(survey, 'CompletedDate', None),
        DeliveryDate=getattr(survey, 'DeliveryDate', None),
        DueDate=getattr(survey, 'DueDate', None),
        QuotedPrice=getattr(survey, 'QuotedPrice', None),
        FinalPrice=getattr(survey, 'FinalPrice', None),
        EstimatedCost=getattr(survey, 'EstimatedCost', None),
        ActualCost=getattr(survey, 'ActualCost', None),
        Notes=getattr(survey, 'Notes', None),
        IsFieldworkComplete=getattr(survey, 'IsFieldworkComplete', None),
        IsDrawingComplete=getattr(survey, 'IsDrawingComplete', None),
        IsScanned=getattr(survey, 'IsScanned', None),
        IsDelivered=getattr(survey, 'IsDelivered', None),
        IsActive=getattr(survey, 'IsActive', True),
        CreatedDate=getattr(survey, 'CreatedDate', None),
        ModifiedDate=getattr(survey, 'ModifiedDate', None),
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
        PropertyId=safe_int(getattr(property, 'PropertyId', None)),
        PropertyCode=getattr(property, 'PropertyCode', None),
        PropertyName=getattr(property, 'PropertyName', None),
        PropertyDescription=getattr(property, 'PropertyDescription', None),
        OwnerName=getattr(property, 'OwnerName', None),
        OwnerPhone=getattr(property, 'OwnerPhone', None),
        OwnerEmail=getattr(property, 'OwnerEmail', None),
        AddressId=safe_int(getattr(property, 'AddressId', None)),
        TownshipId=safe_int(getattr(property, 'TownshipId', None)),
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

class Query(ObjectType):
    surveys = Field(SurveyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    survey = Field(SurveyType, surveyId=String(required=True))
    customers = Field(CustomerListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    customer = Field(CustomerType, customerId=String(required=True))
    properties = Field(PropertyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    property = Field(PropertyType, propertyId=String(required=True))
    townships = Field(TownshipListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    township = Field(TownshipType, townshipId=String(required=True))

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

class PropertyInput(graphene.InputObjectType):
    PropertyCode = String(required=True)  # Required in models.py
    PropertyName = String(required=True)  # Required in models.py
    PropertyDescription = String()
    OwnerName = String()
    OwnerPhone = String()
    OwnerEmail = String()
    AddressId = String()  # String in models.py, not Int
    TownshipId = String()  # String in models.py, not Int

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

class CreatePropertyMutation(graphene.Mutation):
    class Arguments:
        input = PropertyInput(required=True)
    
    # Return fields that frontend expects, even if they don't exist in models.py Property
    PropertyId = String()  # String in models.py but frontend might expect Int
    SurveyPrimaryKey = Int()  # Frontend expects this
    LegacyTax = String()  # Frontend expects this
    District = String()  # Frontend expects this  
    Section = String()  # Frontend expects this
    Block = String()  # Frontend expects this
    Lot = String()  # Frontend expects this
    AddressId = String()  # String in models.py
    TownshipId = String()  # String in models.py
    PropertyType = String()  # Frontend expects this
    CreatedDate = DateTime()
    ModifiedDate = DateTime()
    
    def mutate(self, info, input):
        try:
            from models import Property
            # Create Property using models.py Property class directly
            property_data = Property(**input)
            property = crud.create_property(property=property_data)
            if property:
                return CreatePropertyMutation(
                    PropertyId=getattr(property, 'PropertyId', ''),
                    SurveyPrimaryKey=0,  # Default value since not in models.py Property
                    LegacyTax='',  # Default value since not in models.py Property
                    District='',  # Default value since not in models.py Property
                    Section='',  # Default value since not in models.py Property
                    Block='',  # Default value since not in models.py Property
                    Lot='',  # Default value since not in models.py Property
                    AddressId=getattr(property, 'AddressId', ''),
                    TownshipId=getattr(property, 'TownshipId', ''),
                    PropertyType='Residential',  # Default value since not in models.py Property
                    CreatedDate=getattr(property, 'CreatedDate', None),
                    ModifiedDate=getattr(property, 'ModifiedDate', None)
                )
            return None
        except Exception as e:
            print(f"Error creating property: {e}")
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

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomerMutation.Field()
    createProperty = CreatePropertyMutation.Field()
    create_township = CreateTownshipMutation.Field()
    update_township = UpdateTownshipMutation.Field()
    delete_township = DeleteTownshipMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)