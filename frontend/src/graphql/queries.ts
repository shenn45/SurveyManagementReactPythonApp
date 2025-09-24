import { gql } from '@apollo/client';

// Customer Queries
export const GET_CUSTOMERS = gql`
  query GetCustomers($skip: Int = 0, $limit: Int = 100, $search: String) {
    customers(skip: $skip, limit: $limit, search: $search) {
      customers {
        CustomerId
        CustomerCode
        CompanyName
        ContactFirstName
        ContactLastName
        Email
        Phone
        Fax
        Website
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
      total
      page
      size
    }
  }
`;

export const GET_CUSTOMER = gql`
  query GetCustomer($customerId: String!) {
    customer(customerId: $customerId) {
      CustomerId
      CustomerCode
      CompanyName
      ContactFirstName
      ContactLastName
      Email
      Phone
      Fax
      Website
      IsActive
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

// Customer Mutations
export const CREATE_CUSTOMER = gql`
  mutation CreateCustomer($input: CreateCustomerInput!) {
    createCustomer(input: $input) {
      customer {
        CustomerId
        CustomerCode
        CompanyName
        ContactFirstName
        ContactLastName
        Email
        Phone
        Fax
        Website
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const UPDATE_CUSTOMER = gql`
  mutation UpdateCustomer($customerId: String!, $input: CustomerUpdateInput!) {
    updateCustomer(customerId: $customerId, input: $input) {
      customer {
        CustomerId
        CustomerCode
        CompanyName
        ContactFirstName
        ContactLastName
        Email
        Phone
        Fax
        Website
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const DELETE_CUSTOMER = gql`
  mutation DeleteCustomer($customerId: String!) {
    deleteCustomer(customerId: $customerId) {
      success
    }
  }
`;

// Survey Queries
export const GET_SURVEYS = gql`
  query GetSurveys($skip: Int = 0, $limit: Int = 100, $search: String) {
    surveys(skip: $skip, limit: $limit, search: $search) {
      surveys {
        SurveyId
        SurveyNumber
        CustomerId
        PropertyId
        SurveyTypeId
        StatusId
        Title
        Description
        PurposeCode
        RequestDate
        ScheduledDate
        CompletedDate
        DeliveryDate
        DueDate
        QuotedPrice
        FinalPrice
        IsFieldworkComplete
        IsDrawingComplete
        IsScanned
        IsDelivered
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
      total
      page
      size
    }
  }
`;

export const GET_SURVEY = gql`
  query GetSurvey($surveyId: String!) {
    survey(surveyId: $surveyId) {
      SurveyId
      SurveyNumber
      CustomerId
      PropertyId
      SurveyTypeId
      StatusId
      Title
      Description
      PurposeCode
      RequestDate
      ScheduledDate
      CompletedDate
      DeliveryDate
      DueDate
      QuotedPrice
      FinalPrice
      IsFieldworkComplete
      IsDrawingComplete
      IsScanned
      IsDelivered
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

// Survey Mutations
export const CREATE_SURVEY = gql`
  mutation CreateSurvey($input: SurveyInput!) {
    createSurvey(input: $input) {
      survey {
        SurveyId
        SurveyNumber
        CustomerId
        PropertyId
        SurveyTypeId
        StatusId
        Title
        Description
        PurposeCode
        RequestDate
        ScheduledDate
        CompletedDate
        DeliveryDate
        DueDate
        QuotedPrice
        FinalPrice
        IsFieldworkComplete
        IsDrawingComplete
        IsScanned
        IsDelivered
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const UPDATE_SURVEY = gql`
  mutation UpdateSurvey($surveyId: String!, $input: SurveyUpdateInput!) {
    updateSurvey(surveyId: $surveyId, input: $input) {
      survey {
        SurveyId
        SurveyNumber
        CustomerId
        PropertyId
        SurveyTypeId
        StatusId
        Title
        Description
        PurposeCode
        RequestDate
        ScheduledDate
        CompletedDate
        DeliveryDate
        DueDate
        QuotedPrice
        FinalPrice
        IsFieldworkComplete
        IsDrawingComplete
        IsScanned
        IsDelivered
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const DELETE_SURVEY = gql`
  mutation DeleteSurvey($surveyId: String!) {
    deleteSurvey(surveyId: $surveyId)
  }
`;

// Property Queries
export const GET_PROPERTIES = gql`
  query GetProperties($skip: Int = 0, $limit: Int = 100, $search: String) {
    properties(skip: $skip, limit: $limit, search: $search) {
      properties {
        PropertyId
        PropertyCode
        PropertyName
        PropertyDescription
        OwnerName
        OwnerPhone
        OwnerEmail
        SurveyPrimaryKey
        LegacyTax
        District
        Section
        Block
        Lot
        AddressId
        TownshipId
        PropertyType
        IsActive
        CreatedDate
        ModifiedDate
      }
      total
      page
      size
    }
  }
`;

export const GET_PROPERTY = gql`
  query GetProperty($propertyId: String!) {
    property(propertyId: $propertyId) {
      PropertyId
      PropertyCode
      PropertyName
      PropertyDescription
      OwnerName
      OwnerPhone
      OwnerEmail
      SurveyPrimaryKey
      LegacyTax
      District
      Section
      Block
      Lot
      AddressId
      TownshipId
      PropertyType
      IsActive
      CreatedDate
      ModifiedDate
    }
  }
`;

// Property Mutations
export const CREATE_PROPERTY = gql`
  mutation CreateProperty($input: PropertyInput!) {
    createProperty(input: $input) {
      property {
        PropertyId
        PropertyCode
        PropertyName
        PropertyDescription
        OwnerName
        OwnerPhone
        OwnerEmail
        SurveyPrimaryKey
        LegacyTax
        District
        Section
        Block
        Lot
        AddressId
        TownshipId
        PropertyType
        IsActive
        CreatedDate
        ModifiedDate
      }
    }
  }
`;

export const UPDATE_PROPERTY = gql`
  mutation UpdateProperty($propertyId: String!, $input: PropertyUpdateInput!) {
    updateProperty(propertyId: $propertyId, input: $input) {
      property {
        PropertyId
        PropertyCode
        PropertyName
        PropertyDescription
        OwnerName
        OwnerPhone
        OwnerEmail
        SurveyPrimaryKey
        LegacyTax
        District
        Section
        Block
        Lot
        AddressId
        TownshipId
        PropertyType
        IsActive
        CreatedDate
        ModifiedDate
      }
    }
  }
`;

export const DELETE_PROPERTY = gql`
  mutation DeleteProperty($propertyId: String!) {
    deleteProperty(propertyId: $propertyId) {
      success
    }
  }
`;

// Lookup Queries
export const GET_SURVEY_TYPES = gql`
  query GetSurveyTypes {
    surveyTypes {
      SurveyTypeId
      SurveyTypeName
      Description
      IsActive
    }
  }
`;

export const GET_SURVEY_STATUSES = gql`
  query GetSurveyStatuses {
    surveyStatuses {
      SurveyStatusId
      StatusName
      Description
      IsActive
    }
  }
`;

export const CREATE_SURVEY_STATUS = gql`
  mutation CreateSurveyStatus($input: CreateSurveyStatusInput!) {
    createSurveyStatus(input: $input) {
      surveyStatus {
        SurveyStatusId
        StatusName
        Description
        IsActive
      }
    }
  }
`;

export const UPDATE_SURVEY_STATUS = gql`
  mutation UpdateSurveyStatus($surveyStatusId: String!, $input: UpdateSurveyStatusInput!) {
    updateSurveyStatus(surveyStatusId: $surveyStatusId, input: $input) {
      surveyStatus {
        SurveyStatusId
        StatusName
        Description
        IsActive
      }
    }
  }
`;

export const GET_TOWNSHIPS = gql`
  query GetTownships($skip: Int = 0, $limit: Int = 100, $search: String) {
    townships(skip: $skip, limit: $limit, search: $search) {
      townships {
        TownshipId
        TownshipName
        County
        State
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
      total
      page
      size
    }
  }
`;

export const GET_TOWNSHIP = gql`
  query GetTownship($townshipId: String!) {
    township(townshipId: $townshipId) {
      TownshipId
      TownshipName
      County
      State
      IsActive
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

export const CREATE_TOWNSHIP = gql`
  mutation CreateTownship($input: TownshipInput!) {
    createTownship(input: $input) {
      township {
        TownshipId
        TownshipName
        County
        State
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const UPDATE_TOWNSHIP = gql`
  mutation UpdateTownship($townshipId: String!, $input: TownshipUpdateInput!) {
    updateTownship(townshipId: $townshipId, input: $input) {
      township {
        TownshipId
        TownshipName
        County
        State
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const DELETE_TOWNSHIP = gql`
  mutation DeleteTownship($townshipId: String!) {
    deleteTownship(townshipId: $townshipId) {
      success
    }
  }
`;

// Board Configuration Queries
export const GET_BOARD_CONFIGURATIONS = gql`
  query GetBoardConfigurations {
    boardConfigurations {
      BoardConfigId
      BoardName
      BoardSlug
      Description
      UserId
      IsDefault
      IsActive
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

export const GET_BOARD_CONFIGURATION = gql`
  query GetBoardConfiguration($boardConfigId: String!) {
    boardConfiguration(boardConfigId: $boardConfigId) {
      BoardConfigId
      BoardName
      BoardSlug
      Description
      UserId
      IsDefault
      IsActive
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

export const GET_BOARD_CONFIGURATION_BY_SLUG = gql`
  query GetBoardConfigurationBySlug($boardSlug: String!) {
    boardConfigurationBySlug(boardSlug: $boardSlug) {
      BoardConfigId
      BoardName
      BoardSlug
      Description
      UserId
      IsDefault
      IsActive
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

export const GET_DEFAULT_BOARD_CONFIGURATION = gql`
  query GetDefaultBoardConfiguration {
    defaultBoardConfiguration {
      BoardConfigId
      BoardName
      BoardSlug
      Description
      UserId
      IsDefault
      IsActive
      CreatedDate
      ModifiedDate
      CreatedBy
      ModifiedBy
    }
  }
`;

// Board Configuration Mutations
export const CREATE_BOARD_CONFIGURATION = gql`
  mutation CreateBoardConfiguration($boardConfig: BoardConfigurationInput!) {
    createBoardConfiguration(boardConfig: $boardConfig) {
      boardConfiguration {
        BoardConfigId
        BoardName
        BoardSlug
        Description
        UserId
        IsDefault
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const UPDATE_BOARD_CONFIGURATION = gql`
  mutation UpdateBoardConfiguration($boardConfigId: String!, $boardConfig: BoardConfigurationUpdateInput!) {
    updateBoardConfiguration(boardConfigId: $boardConfigId, boardConfig: $boardConfig) {
      boardConfiguration {
        BoardConfigId
        BoardName
        BoardSlug
        Description
        UserId
        IsDefault
        IsActive
        CreatedDate
        ModifiedDate
        CreatedBy
        ModifiedBy
      }
    }
  }
`;

export const DELETE_BOARD_CONFIGURATION = gql`
  mutation DeleteBoardConfiguration($boardConfigId: String!) {
    deleteBoardConfiguration(boardConfigId: $boardConfigId) {
      success
    }
  }
`;
