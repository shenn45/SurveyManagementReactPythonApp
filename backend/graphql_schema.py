import graphene
from graphene import ObjectType, List, Field, String, Int, Boolean, Float, DateTime, InputObjectType
from typing import Optional
from datetime import datetime

import crud
from database import get_db


# Utility function to get database session
def get_db_session():
    return next(get_db())


# GraphQL Types
class CustomerType(ObjectType):
    CustomerId = Int()
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


class SurveyType(ObjectType):
    SurveyId = Int()
    SurveyNumber = String()
    CustomerId = Int()
    PropertyId = Int()
    SurveyTypeId = Int()
    StatusId = Int()
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
    IsFieldworkComplete = Boolean()
    IsDrawingComplete = Boolean()
    IsScanned = Boolean()
    IsDelivered = Boolean()
    CreatedDate = DateTime()
    ModifiedDate = DateTime()
    CreatedBy = String()
    ModifiedBy = String()


class PropertyType(ObjectType):
    PropertyId = Int()
    SurveyPrimaryKey = Int()
    LegacyTax = String()
    District = String()
    Section = String()
    Block = String()
    Lot = String()
    AddressId = Int()
    TownshipId = Int()
    PropertyType_field = String()
    CreatedDate = DateTime()
    ModifiedDate = DateTime()


class SurveyTypeClass(ObjectType):
    SurveyTypeId = Int()
    TypeName = String()
    TypeDescription = String()
    EstimatedDuration = Int()
    BasePrice = Float()
    IsActive = Boolean()


class SurveyStatusType(ObjectType):
    StatusId = Int()
    StatusCode = String()
    StatusName = String()
    SortOrder = Int()
    IsActive = Boolean()


class TownshipType(ObjectType):
    TownshipId = Int()
    Name = String()
    FoilMethod = String()
    Website = String()
    Description = String()


# Response Types for Pagination
class CustomerListResponse(ObjectType):
    customers = List(CustomerType)
    total = Int()
    page = Int()
    size = Int()


class SurveyListResponse(ObjectType):
    surveys = List(SurveyType)
    total = Int()
    page = Int()
    size = Int()


class PropertyListResponse(ObjectType):
    properties = List(PropertyType)
    total = Int()
    page = Int()
    size = Int()


# Input Types for Mutations
class CustomerInput(InputObjectType):
    CustomerCode = String(required=True)
    CompanyName = String(required=True)
    ContactFirstName = String()
    ContactLastName = String()
    Email = String()
    Phone = String()
    Fax = String()
    Website = String()
    IsActive = Boolean(default_value=True)


class CustomerUpdateInput(InputObjectType):
    CustomerCode = String()
    CompanyName = String()
    ContactFirstName = String()
    ContactLastName = String()
    Email = String()
    Phone = String()
    Fax = String()
    Website = String()
    IsActive = Boolean()


class SurveyInput(InputObjectType):
    SurveyNumber = String(required=True)
    CustomerId = Int()
    PropertyId = Int()
    SurveyTypeId = Int()
    StatusId = Int(required=True)
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
    IsFieldworkComplete = Boolean(default_value=False)
    IsDrawingComplete = Boolean(default_value=False)
    IsScanned = Boolean(default_value=False)
    IsDelivered = Boolean(default_value=False)


class SurveyUpdateInput(InputObjectType):
    SurveyNumber = String()
    CustomerId = Int()
    PropertyId = Int()
    SurveyTypeId = Int()
    StatusId = Int()
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
    IsFieldworkComplete = Boolean()
    IsDrawingComplete = Boolean()
    IsScanned = Boolean()
    IsDelivered = Boolean()


class PropertyInput(InputObjectType):
    SurveyPrimaryKey = Int(required=True)
    LegacyTax = String()
    District = String()
    Section = String()
    Block = String()
    Lot = String()
    AddressId = Int()
    TownshipId = Int()
    PropertyType_field = String()


class PropertyUpdateInput(InputObjectType):
    SurveyPrimaryKey = Int()
    LegacyTax = String()
    District = String()
    Section = String()
    Block = String()
    Lot = String()
    AddressId = Int()
    TownshipId = Int()
    PropertyType_field = String()


# Convert model to GraphQL type
def model_to_customer(customer_model):
    return CustomerType(
        CustomerId=customer_model.CustomerId,
        CustomerCode=customer_model.CustomerCode,
        CompanyName=customer_model.CompanyName,
        ContactFirstName=customer_model.ContactFirstName,
        ContactLastName=customer_model.ContactLastName,
        Email=customer_model.Email,
        Phone=customer_model.Phone,
        Fax=customer_model.Fax,
        Website=customer_model.Website,
        IsActive=customer_model.IsActive,
        CreatedDate=customer_model.CreatedDate,
        ModifiedDate=customer_model.ModifiedDate,
        CreatedBy=customer_model.CreatedBy,
        ModifiedBy=customer_model.ModifiedBy
    )


def model_to_survey(survey_model):
    return SurveyType(
        SurveyId=survey_model.SurveyId,
        SurveyNumber=survey_model.SurveyNumber,
        CustomerId=survey_model.CustomerId,
        PropertyId=survey_model.PropertyId,
        SurveyTypeId=survey_model.SurveyTypeId,
        StatusId=survey_model.StatusId,
        Title=survey_model.Title,
        Description=survey_model.Description,
        PurposeCode=survey_model.PurposeCode,
        RequestDate=survey_model.RequestDate,
        ScheduledDate=survey_model.ScheduledDate,
        CompletedDate=survey_model.CompletedDate,
        DeliveryDate=survey_model.DeliveryDate,
        DueDate=survey_model.DueDate,
        QuotedPrice=float(survey_model.QuotedPrice) if survey_model.QuotedPrice else None,
        FinalPrice=float(survey_model.FinalPrice) if survey_model.FinalPrice else None,
        IsFieldworkComplete=survey_model.IsFieldworkComplete,
        IsDrawingComplete=survey_model.IsDrawingComplete,
        IsScanned=survey_model.IsScanned,
        IsDelivered=survey_model.IsDelivered,
        CreatedDate=survey_model.CreatedDate,
        ModifiedDate=survey_model.ModifiedDate,
        CreatedBy=survey_model.CreatedBy,
        ModifiedBy=survey_model.ModifiedBy
    )


def model_to_property(property_model):
    return PropertyType(
        PropertyId=property_model.PropertyId,
        SurveyPrimaryKey=property_model.SurveyPrimaryKey,
        LegacyTax=property_model.LegacyTax,
        District=property_model.District,
        Section=property_model.Section,
        Block=property_model.Block,
        Lot=property_model.Lot,
        AddressId=property_model.AddressId,
        TownshipId=property_model.TownshipId,
        PropertyType_field=property_model.PropertyType,
        CreatedDate=property_model.CreatedDate,
        ModifiedDate=property_model.ModifiedDate
    )


def model_to_survey_type(survey_type_model):
    return SurveyTypeClass(
        SurveyTypeId=survey_type_model.SurveyTypeId,
        TypeName=survey_type_model.TypeName,
        TypeDescription=survey_type_model.TypeDescription,
        EstimatedDuration=survey_type_model.EstimatedDuration,
        BasePrice=float(survey_type_model.BasePrice) if survey_type_model.BasePrice else None,
        IsActive=survey_type_model.IsActive
    )


def model_to_survey_status(survey_status_model):
    return SurveyStatusType(
        StatusId=survey_status_model.StatusId,
        StatusCode=survey_status_model.StatusCode,
        StatusName=survey_status_model.StatusName,
        SortOrder=survey_status_model.SortOrder,
        IsActive=survey_status_model.IsActive
    )


def model_to_township(township_model):
    return TownshipType(
        TownshipId=township_model.TownshipId,
        Name=township_model.Name,
        FoilMethod=township_model.FoilMethod,
        Website=township_model.Website,
        Description=township_model.Description
    )


class Query(ObjectType):
    customers = Field(CustomerListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    customer = Field(CustomerType, customer_id=Int(required=True))
    surveys = Field(SurveyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    survey = Field(SurveyType, survey_id=Int(required=True))
    properties = Field(PropertyListResponse, skip=Int(default_value=0), limit=Int(default_value=100), search=String())
    property = Field(PropertyType, property_id=Int(required=True))
    survey_types = List(SurveyTypeClass)
    survey_statuses = List(SurveyStatusType)
    townships = List(TownshipType)

    def resolve_customers(self, info, skip=0, limit=100, search=None):
        db = get_db_session()
        try:
            customers_data, total = crud.get_customers(db, skip=skip, limit=limit, search=search)
            customers = [model_to_customer(c) for c in customers_data]
            return CustomerListResponse(
                customers=customers,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        finally:
            db.close()

    def resolve_customer(self, info, customer_id):
        db = get_db_session()
        try:
            customer_data = crud.get_customer(db, customer_id=customer_id)
            return model_to_customer(customer_data) if customer_data else None
        finally:
            db.close()

    def resolve_surveys(self, info, skip=0, limit=100, search=None):
        db = get_db_session()
        try:
            surveys_data, total = crud.get_surveys(db, skip=skip, limit=limit, search=search)
            surveys = [model_to_survey(s) for s in surveys_data]
            return SurveyListResponse(
                surveys=surveys,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        finally:
            db.close()

    def resolve_survey(self, info, survey_id):
        db = get_db_session()
        try:
            survey_data = crud.get_survey(db, survey_id=survey_id)
            return model_to_survey(survey_data) if survey_data else None
        finally:
            db.close()

    def resolve_properties(self, info, skip=0, limit=100, search=None):
        db = get_db_session()
        try:
            properties_data, total = crud.get_properties(db, skip=skip, limit=limit, search=search)
            properties = [model_to_property(p) for p in properties_data]
            return PropertyListResponse(
                properties=properties,
                total=total,
                page=skip // limit + 1,
                size=limit
            )
        finally:
            db.close()

    def resolve_property(self, info, property_id):
        db = get_db_session()
        try:
            property_data = crud.get_property(db, property_id=property_id)
            return model_to_property(property_data) if property_data else None
        finally:
            db.close()

    def resolve_survey_types(self, info):
        db = get_db_session()
        try:
            survey_types_data = crud.get_survey_types(db)
            return [model_to_survey_type(st) for st in survey_types_data]
        finally:
            db.close()

    def resolve_survey_statuses(self, info):
        db = get_db_session()
        try:
            survey_statuses_data = crud.get_survey_statuses(db)
            return [model_to_survey_status(ss) for ss in survey_statuses_data]
        finally:
            db.close()

    def resolve_townships(self, info):
        db = get_db_session()
        try:
            townships_data = crud.get_townships(db)
            return [model_to_township(t) for t in townships_data]
        finally:
            db.close()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = Field(CustomerType)

    def mutate(self, info, input):
        db = get_db_session()
        try:
            from schemas import CustomerCreate
            customer_data = CustomerCreate(**input)
            customer = crud.create_customer(db=db, customer=customer_data)
            return CreateCustomer(customer=model_to_customer(customer))
        finally:
            db.close()


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        customer_id = Int(required=True)
        input = CustomerUpdateInput(required=True)

    customer = Field(CustomerType)

    def mutate(self, info, customer_id, input):
        db = get_db_session()
        try:
            from schemas import CustomerUpdate
            # Filter out None values
            update_data = {k: v for k, v in input.items() if v is not None}
            customer_data = CustomerUpdate(**update_data)
            customer = crud.update_customer(db=db, customer_id=customer_id, customer=customer_data)
            return UpdateCustomer(customer=model_to_customer(customer) if customer else None)
        finally:
            db.close()


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        customer_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, customer_id):
        db = get_db_session()
        try:
            customer = crud.delete_customer(db=db, customer_id=customer_id)
            return DeleteCustomer(success=customer is not None)
        finally:
            db.close()


class CreateSurvey(graphene.Mutation):
    class Arguments:
        input = SurveyInput(required=True)

    survey = Field(SurveyType)

    def mutate(self, info, input):
        db = get_db_session()
        try:
            from schemas import SurveyCreate
            survey_data = SurveyCreate(**input)
            survey = crud.create_survey(db=db, survey=survey_data)
            return CreateSurvey(survey=model_to_survey(survey))
        finally:
            db.close()


class UpdateSurvey(graphene.Mutation):
    class Arguments:
        survey_id = Int(required=True)
        input = SurveyUpdateInput(required=True)

    survey = Field(SurveyType)

    def mutate(self, info, survey_id, input):
        db = get_db_session()
        try:
            from schemas import SurveyUpdate
            # Filter out None values
            update_data = {k: v for k, v in input.items() if v is not None}
            survey_data = SurveyUpdate(**update_data)
            survey = crud.update_survey(db=db, survey_id=survey_id, survey=survey_data)
            return UpdateSurvey(survey=model_to_survey(survey) if survey else None)
        finally:
            db.close()


class DeleteSurvey(graphene.Mutation):
    class Arguments:
        survey_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, survey_id):
        db = get_db_session()
        try:
            survey = crud.delete_survey(db=db, survey_id=survey_id)
            return DeleteSurvey(success=survey is not None)
        finally:
            db.close()


class CreateProperty(graphene.Mutation):
    class Arguments:
        input = PropertyInput(required=True)

    property = Field(PropertyType)

    def mutate(self, info, input):
        db = get_db_session()
        try:
            from schemas import PropertyCreate
            # Map PropertyType_field to PropertyType
            input_dict = dict(input)
            if 'PropertyType_field' in input_dict:
                input_dict['PropertyType'] = input_dict.pop('PropertyType_field')
            property_data = PropertyCreate(**input_dict)
            property = crud.create_property(db=db, property=property_data)
            return CreateProperty(property=model_to_property(property))
        finally:
            db.close()


class UpdateProperty(graphene.Mutation):
    class Arguments:
        property_id = Int(required=True)
        input = PropertyUpdateInput(required=True)

    property = Field(PropertyType)

    def mutate(self, info, property_id, input):
        db = get_db_session()
        try:
            from schemas import PropertyUpdate
            # Filter out None values and map PropertyType_field to PropertyType
            update_data = {k: v for k, v in input.items() if v is not None}
            if 'PropertyType_field' in update_data:
                update_data['PropertyType'] = update_data.pop('PropertyType_field')
            property_data = PropertyUpdate(**update_data)
            property = crud.update_property(db=db, property_id=property_id, property=property_data)
            return UpdateProperty(property=model_to_property(property) if property else None)
        finally:
            db.close()


class DeleteProperty(graphene.Mutation):
    class Arguments:
        property_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, property_id):
        db = get_db_session()
        try:
            property = crud.delete_property(db=db, property_id=property_id)
            return DeleteProperty(success=property is not None)
        finally:
            db.close()


class Mutation(ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()
    create_survey = CreateSurvey.Field()
    update_survey = UpdateSurvey.Field()
    delete_survey = DeleteSurvey.Field()
    create_property = CreateProperty.Field()
    update_property = UpdateProperty.Field()
    delete_property = DeleteProperty.Field()


# Create the GraphQL schema
schema = graphene.Schema(query=Query, mutation=Mutation)