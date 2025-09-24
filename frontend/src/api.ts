import axios from 'axios';
import {
  Customer,
  CustomerCreate,
  CustomerListResponse,
  Survey,
  SurveyCreate,
  SurveyListResponse,
  Property,
  PropertyCreate,
  PropertyListResponse,
  SurveyType,
  SurveyStatus,
  Township,
  UserSettings,
  UserSettingsUpdate
} from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Customer API
export const customerApi = {
  getAll: (page = 1, size = 100, search?: string): Promise<CustomerListResponse> =>
    api.get('/customers', { params: { skip: (page - 1) * size, limit: size, search } })
      .then(response => response.data),
  
  getById: (id: number): Promise<Customer> =>
    api.get(`/customers/${id}`).then(response => response.data),
  
  create: (customer: CustomerCreate): Promise<Customer> =>
    api.post('/customers', customer).then(response => response.data),
  
  update: (id: number, customer: Partial<CustomerCreate>): Promise<Customer> =>
    api.put(`/customers/${id}`, customer).then(response => response.data),
  
  delete: (id: number): Promise<void> =>
    api.delete(`/customers/${id}`).then(response => response.data),
};

// Survey API
export const surveyApi = {
  getAll: (page = 1, size = 100, search?: string): Promise<SurveyListResponse> =>
    api.get('/surveys', { params: { skip: (page - 1) * size, limit: size, search } })
      .then(response => response.data),
  
  getById: (id: number): Promise<Survey> =>
    api.get(`/surveys/${id}`).then(response => response.data),
  
  create: (survey: SurveyCreate): Promise<Survey> =>
    api.post('/surveys', survey).then(response => response.data),
  
  update: (id: number, survey: Partial<SurveyCreate>): Promise<Survey> =>
    api.put(`/surveys/${id}`, survey).then(response => response.data),
  
  delete: (id: number): Promise<void> =>
    api.delete(`/surveys/${id}`).then(response => response.data),
};

// Property API
export const propertyApi = {
  getAll: (page = 1, size = 100, search?: string): Promise<PropertyListResponse> =>
    api.get('/properties', { params: { skip: (page - 1) * size, limit: size, search } })
      .then(response => response.data),
  
  getById: (id: number): Promise<Property> =>
    api.get(`/properties/${id}`).then(response => response.data),
  
  create: (property: PropertyCreate): Promise<Property> =>
    api.post('/properties', property).then(response => response.data),
  
  update: (id: number, property: Partial<PropertyCreate>): Promise<Property> =>
    api.put(`/properties/${id}`, property).then(response => response.data),
  
  delete: (id: number): Promise<void> =>
    api.delete(`/properties/${id}`).then(response => response.data),
};

// Lookup API
export const lookupApi = {
  getSurveyTypes: (): Promise<SurveyType[]> =>
    api.get('/lookup/survey-types').then(response => response.data),
  
  getSurveyStatuses: (): Promise<SurveyStatus[]> =>
    api.get('/lookup/survey-statuses').then(response => response.data),
  
  getTownships: (): Promise<Township[]> =>
    api.get('/lookup/townships').then(response => response.data),
};

// User Settings API
export const userSettingsApi = {
  getSettings: (settingsType: string): Promise<UserSettings> =>
    api.get(`/user-settings/${settingsType}`).then(response => response.data),
  
  getAllSettings: (): Promise<UserSettings[]> =>
    api.get('/user-settings').then(response => response.data),
  
  upsertSettings: (settingsType: string, settingsData: Record<string, any>): Promise<UserSettings> =>
    api.put(`/user-settings/${settingsType}/upsert`, settingsData).then(response => response.data),
  
  updateSettings: (settingsType: string, settingsData: UserSettingsUpdate): Promise<UserSettings> =>
    api.put(`/user-settings/${settingsType}`, settingsData).then(response => response.data),
  
  deleteSettings: (settingsType: string): Promise<void> =>
    api.delete(`/user-settings/${settingsType}`).then(response => response.data),
};
