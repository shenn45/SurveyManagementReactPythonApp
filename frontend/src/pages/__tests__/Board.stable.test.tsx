import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Board from '../Board';

// Create stable mock functions outside component to prevent recreating on each render
const mockRefetch = jest.fn();
const mockCreateSurvey = jest.fn();
const mockUpdateSurvey = jest.fn();
const mockCreateSurveyStatus = jest.fn();
const mockUpdateSurveyStatus = jest.fn();

jest.mock('../../hooks/useGraphQLApi', () => ({
  useSurveys: () => ({
    data: [
      {
        survey_id: '1',
        survey_name: 'Property Survey #1',
        survey_status_id: 'draft',
        customer_id: 'customer-1',
        description: 'Test survey',
        created_at: '2024-01-01',
        updated_at: '2024-01-01'
      }
    ],
    loading: false,
    error: null,
    refetch: mockRefetch,
  }),
  useSurveyStatuses: () => ({
    data: [
      { status_id: 'draft', StatusName: 'Draft', status_order: 1, IsActive: true, SurveyStatusId: 'draft' },
      { status_id: 'in-progress', StatusName: 'In Progress', status_order: 2, IsActive: true, SurveyStatusId: 'in-progress' },
      { status_id: 'completed', StatusName: 'Completed', status_order: 3, IsActive: true, SurveyStatusId: 'completed' }
    ],
    loading: false,
    error: null,
    refetch: mockRefetch,
  }),
  useCustomers: () => ({
    data: [
      { customer_id: 'customer-1', customer_name: 'Test Customer', email: 'test@example.com' }
    ],
    loading: false,
    error: null,
    refetch: mockRefetch,
  }),
  useSurveyTypes: () => ({
    data: [
      { survey_type_id: 'property', survey_type_name: 'Property Survey' }
    ],
    loading: false,
    error: null,
    refetch: mockRefetch,
  }),
  useCreateSurvey: () => [mockCreateSurvey, { loading: false }],
  useUpdateSurvey: () => [mockUpdateSurvey, { loading: false }],
  useCreateSurveyStatus: () => [mockCreateSurveyStatus, { loading: false }],
  useUpdateSurveyStatus: () => [mockUpdateSurveyStatus, { loading: false }],
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(() => null),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true,
});

const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

describe('Board Component - Stable Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
  });

  it('renders without infinite loops', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    // Wait for the component to stabilize
    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    }, { timeout: 3000 });

    // Check that we don't have excessive localStorage calls (which would indicate infinite loops)
    expect(localStorageMock.setItem).toHaveBeenCalledTimes(2); // Once for column order, once for hidden columns
  });

  it('displays survey status columns', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Draft')).toBeInTheDocument();
      expect(screen.getByText('In Progress')).toBeInTheDocument();
      expect(screen.getByText('Completed')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('shows create new survey button', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Create New Survey')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('shows manage columns button', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Manage Columns')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('has proper page heading', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 1, name: /survey board/i })).toBeInTheDocument();
    }, { timeout: 3000 });
  });
});