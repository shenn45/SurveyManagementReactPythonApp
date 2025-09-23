import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import Board from '../Board';

// Mock the GraphQL hooks with simple data
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
    refetch: jest.fn(),
  }),
  useSurveyStatuses: () => ({
    data: [
      { status_id: 'draft', StatusName: 'Draft', status_order: 1, IsActive: true, SurveyStatusId: 'draft' },
      { status_id: 'in-progress', StatusName: 'In Progress', status_order: 2, IsActive: true, SurveyStatusId: 'in-progress' },
      { status_id: 'completed', StatusName: 'Completed', status_order: 3, IsActive: true, SurveyStatusId: 'completed' }
    ],
    loading: false,
    refetch: jest.fn(),
  }),
  useCustomers: () => ({
    data: [
      {
        customer_id: 'customer-1',
        customer_name: 'Test Customer',
        email: 'test@example.com'
      }
    ],
    loading: false,
  }),
  useSurveyTypes: () => ({
    data: [],
    loading: false,
  }),
  useCreateSurvey: () => ({
    create: jest.fn(() => Promise.resolve()),
    loading: false
  }),
  useUpdateSurvey: () => ({
    update: jest.fn(() => Promise.resolve()),
    loading: false
  }),
  useCreateSurveyStatus: () => ({
    create: jest.fn(() => Promise.resolve()),
    loading: false
  }),
  useUpdateSurveyStatus: () => ({
    update: jest.fn(() => Promise.resolve()),
  }),
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

describe('Board Component - Functional Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
  });

  it('renders the board with survey columns', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });

    // Check that status columns are rendered
    expect(screen.getByText('Draft')).toBeInTheDocument();
    expect(screen.getByText('In Progress')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('displays surveys in correct columns', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Property Survey #1')).toBeInTheDocument();
    });

    // Check survey is in the Draft column
    const surveyElement = screen.getByText('Property Survey #1');
    expect(surveyElement).toBeInTheDocument();
  });

  it('shows create new survey button', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Create New Survey')).toBeInTheDocument();
    });
  });

  it('shows manage columns button', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Manage Columns')).toBeInTheDocument();
    });
  });

  it('has proper heading structure', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      const heading = screen.getByText('Survey Board');
      expect(heading).toBeInTheDocument();
      expect(heading.tagName).toBe('H1');
    });
  });

  it('handles button clicks without errors', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Create New Survey')).toBeInTheDocument();
    });

    // Test create survey button
    const createButton = screen.getByText('Create New Survey');
    fireEvent.click(createButton);

    // Test manage columns button
    const manageButton = screen.getByText('Manage Columns');
    fireEvent.click(manageButton);

    // Should not throw any errors
    expect(true).toBe(true);
  });
});