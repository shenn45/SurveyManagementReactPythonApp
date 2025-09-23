import { Survey, SurveyStatus, Customer, SurveyType } from '../../types';

export const mockSurveyStatuses: SurveyStatus[] = [
  {
    SurveyStatusId: 'status-1',
    StatusName: 'Pending',
    Description: 'Survey is pending',
    IsActive: true
  },
  {
    SurveyStatusId: 'status-2',
    StatusName: 'In Progress',
    Description: 'Survey is in progress',
    IsActive: true
  },
  {
    SurveyStatusId: 'status-3',
    StatusName: 'Completed',
    Description: 'Survey is completed',
    IsActive: true
  },
  {
    SurveyStatusId: 'status-4',
    StatusName: 'On Hold',
    Description: 'Survey is on hold',
    IsActive: true
  }
];

export const mockCustomers: Customer[] = [
  {
    CustomerId: 'customer-1',
    CustomerCode: 'CUST001',
    CompanyName: 'John Doe Construction',
    ContactFirstName: 'John',
    ContactLastName: 'Doe',
    Email: 'john@example.com',
    Phone: '123-456-7890',
    IsActive: true,
    CreatedDate: '2024-01-01T00:00:00Z',
    ModifiedDate: '2024-01-01T00:00:00Z'
  },
  {
    CustomerId: 'customer-2',
    CustomerCode: 'CUST002',
    CompanyName: 'Jane Smith Engineering',
    ContactFirstName: 'Jane',
    ContactLastName: 'Smith',
    Email: 'jane@example.com',
    Phone: '987-654-3210',
    IsActive: true,
    CreatedDate: '2024-01-01T00:00:00Z',
    ModifiedDate: '2024-01-01T00:00:00Z'
  }
];

export const mockSurveyTypes: SurveyType[] = [
  {
    SurveyTypeId: 'type-1',
    SurveyTypeName: 'Boundary Survey',
    Description: 'Property boundary survey',
    IsActive: true
  },
  {
    SurveyTypeId: 'type-2',
    SurveyTypeName: 'Topographic Survey',
    Description: 'Topographic survey',
    IsActive: true
  }
];

export const mockSurveys: Survey[] = [
  {
    SurveyId: 'survey-1',
    SurveyNumber: 'S001',
    CustomerId: 'customer-1',
    PropertyId: 'property-1',
    SurveyTypeId: 'type-1',
    StatusId: 'status-1',
    Title: 'Boundary Survey for John Doe',
    Description: 'Property boundary survey',
    PurposeCode: 'BOUNDARY',
    RequestDate: '2024-01-01T00:00:00Z',
    ScheduledDate: '2024-01-15T00:00:00Z',
    CompletedDate: undefined,
    DeliveryDate: undefined,
    DueDate: '2024-01-30T00:00:00Z',
    QuotedPrice: 1500,
    FinalPrice: undefined,
    IsFieldworkComplete: false,
    IsDrawingComplete: false,
    IsScanned: false,
    IsDelivered: false,
    CreatedDate: '2024-01-01T00:00:00Z',
    ModifiedDate: '2024-01-01T00:00:00Z',
    notes: [],
    documents: []
  },
  {
    SurveyId: 'survey-2',
    SurveyNumber: 'S002',
    CustomerId: 'customer-2',
    PropertyId: 'property-2',
    SurveyTypeId: 'type-2',
    StatusId: 'status-2',
    Title: 'Topographic Survey for Jane Smith',
    Description: 'Topographic survey',
    PurposeCode: 'TOPO',
    RequestDate: '2024-01-05T00:00:00Z',
    ScheduledDate: '2024-01-20T00:00:00Z',
    CompletedDate: undefined,
    DeliveryDate: undefined,
    DueDate: '2024-02-05T00:00:00Z',
    QuotedPrice: 2000,
    FinalPrice: undefined,
    IsFieldworkComplete: true,
    IsDrawingComplete: false,
    IsScanned: false,
    IsDelivered: false,
    CreatedDate: '2024-01-05T00:00:00Z',
    ModifiedDate: '2024-01-05T00:00:00Z',
    notes: [],
    documents: []
  },
  {
    SurveyId: 'survey-3',
    SurveyNumber: 'S003',
    CustomerId: 'customer-1',
    PropertyId: 'property-3',
    SurveyTypeId: 'type-1',
    StatusId: 'status-3',
    Title: 'Completed Boundary Survey',
    Description: 'Completed boundary survey',
    PurposeCode: 'BOUNDARY',
    RequestDate: '2023-12-01T00:00:00Z',
    ScheduledDate: '2023-12-15T00:00:00Z',
    CompletedDate: '2023-12-20T00:00:00Z',
    DeliveryDate: '2023-12-22T00:00:00Z',
    DueDate: '2023-12-30T00:00:00Z',
    QuotedPrice: 1800,
    FinalPrice: 1750,
    IsFieldworkComplete: true,
    IsDrawingComplete: true,
    IsScanned: true,
    IsDelivered: true,
    CreatedDate: '2023-12-01T00:00:00Z',
    ModifiedDate: '2023-12-20T00:00:00Z',
    notes: [],
    documents: []
  },
  {
    SurveyId: 'survey-4',
    SurveyNumber: 'S004',
    CustomerId: 'customer-2',
    PropertyId: 'property-4',
    SurveyTypeId: 'type-2',
    StatusId: 'unknown-status',
    Title: 'Survey with Unknown Status',
    Description: 'Survey with unknown status',
    PurposeCode: 'OTHER',
    RequestDate: '2024-01-10T00:00:00Z',
    ScheduledDate: undefined,
    CompletedDate: undefined,
    DeliveryDate: undefined,
    DueDate: '2024-02-10T00:00:00Z',
    QuotedPrice: 1200,
    FinalPrice: undefined,
    IsFieldworkComplete: false,
    IsDrawingComplete: false,
    IsScanned: false,
    IsDelivered: false,
    CreatedDate: '2024-01-10T00:00:00Z',
    ModifiedDate: '2024-01-10T00:00:00Z',
    notes: [],
    documents: []
  }
];

export const mockSurveyListResponse = {
  surveys: mockSurveys,
  total: mockSurveys.length
};

export const mockApolloMocks = [
  {
    request: {
      query: require('../../graphql/queries').GET_SURVEYS,
      variables: { skip: 0, limit: 100 }
    },
    result: {
      data: {
        surveys: mockSurveyListResponse
      }
    }
  },
  {
    request: {
      query: require('../../graphql/queries').GET_SURVEY_STATUSES
    },
    result: {
      data: {
        surveyStatuses: mockSurveyStatuses
      }
    }
  },
  {
    request: {
      query: require('../../graphql/queries').GET_CUSTOMERS,
      variables: { skip: 0, limit: 100 }
    },
    result: {
      data: {
        customers: {
          customers: mockCustomers,
          total: mockCustomers.length
        }
      }
    }
  },
  {
    request: {
      query: require('../../graphql/queries').GET_SURVEY_TYPES
    },
    result: {
      data: {
        surveyTypes: mockSurveyTypes
      }
    }
  }
];