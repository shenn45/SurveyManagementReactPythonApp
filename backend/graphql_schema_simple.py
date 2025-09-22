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
    PropertyId = String()
    PropertyNumber = String()
    StreetAddress = String()
    City = String()
    State = String()
    ZipCode = String()
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
    """Convert Property model to GraphQL type"""
    if not property:
        return None
    return PropertyType(
        PropertyId=property.PropertyId,
        PropertyNumber=getattr(property, 'PropertyNumber', None),
        StreetAddress=getattr(property, 'StreetAddress', None),
        City=getattr(property, 'City', None),
        State=getattr(property, 'State', None),
        ZipCode=getattr(property, 'ZipCode', None),
        IsActive=getattr(property, 'IsActive', True),
        CreatedDate=getattr(property, 'CreatedDate', None),
        ModifiedDate=getattr(property, 'ModifiedDate', None),
        CreatedBy=getattr(property, 'CreatedBy', None),
        ModifiedBy=getattr(property, 'ModifiedBy', None)
    )

class Query(ObjectType):
    surveys = Field(SurveyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    survey = Field(SurveyType, surveyId=String(required=True))
    customers = Field(CustomerListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    customer = Field(CustomerType, customerId=String(required=True))
    properties = Field(PropertyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    property = Field(PropertyType, propertyId=String(required=True))

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

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomerMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)