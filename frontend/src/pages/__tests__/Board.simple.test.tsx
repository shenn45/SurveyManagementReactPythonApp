import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MockedProvider } from '@apollo/client/testing';
import { BrowserRouter } from 'react-router-dom';
import Board from '../Board';
import { mockCustomers, mockSurveyStatuses, mockSurveys } from './mockData';

// Mock the GraphQL hooks
jest.mock('../../hooks/useGraphQLApi', () => ({
  useGraphQLApi: () => ({
    surveys: mockSurveys,
    customers: mockCustomers,
    surveyStatuses: mockSurveyStatuses,
    loading: false,
    error: null,
    refetch: jest.fn(),
  }),
  useCreateSurvey: () => [jest.fn(() => Promise.resolve()), { loading: false }],
  useUpdateSurvey: () => [jest.fn(() => Promise.resolve()), { loading: false }],
  useCreateSurveyStatus: () => [jest.fn(() => Promise.resolve()), { loading: false }],
  useUpdateSurveyStatus: () => [jest.fn(() => Promise.resolve()), { loading: false }],
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
    <MockedProvider mocks={[]} addTypename={false}>
      {children}
    </MockedProvider>
  </BrowserRouter>
);

describe('Board Component - Core Functionality', () => {
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

    // Check survey is in correct column
    const draftColumn = screen.getByText('Draft').closest('.bg-gray-100');
    expect(draftColumn).toContainElement(screen.getByText('Property Survey #1'));
  });

  it('handles create new survey button', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Create New Survey')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Create New Survey'));
    
    await waitFor(() => {
      expect(screen.getByText('Create Survey')).toBeInTheDocument();
    });
  });

  it('handles column management button', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Manage Columns')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Manage Columns'));
    
    await waitFor(() => {
      expect(screen.getByText('Create New Status')).toBeInTheDocument();
    });
  });

  it('has proper accessibility structure', async () => {
    render(
      <TestWrapper>
        <Board />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });

    // Check for proper ARIA attributes
    const board = screen.getByRole('main');
    expect(board).toBeInTheDocument();

    // Check for proper heading structure
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
  });
});