import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Board from '../Board';
import * as GraphQLApi from '../../hooks/useGraphQLApi';
import '@testing-library/jest-dom';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Create stable references for mock data to prevent infinite loops
const MOCK_CUSTOMERS = [
  { CustomerId: '1', CustomerName: 'Test Customer', ContactName: 'John Doe' },
  { CustomerId: '2', CustomerName: 'Another Customer', ContactName: 'Jane Smith' }
];

const MOCK_SURVEY_TYPES = [
  { SurveyTypeId: '1', TypeName: 'Property Survey' },
  { SurveyTypeId: '2', TypeName: 'Boundary Survey' }
];

const MOCK_SURVEY_STATUSES = [
  { SurveyStatusId: '1', StatusName: 'New', StatusOrder: 1, IsActive: true },
  { SurveyStatusId: '2', StatusName: 'In Progress', StatusOrder: 2, IsActive: true },
  { SurveyStatusId: '3', StatusName: 'Complete', StatusOrder: 3, IsActive: true }
];

const MOCK_SURVEYS = [
  {
    SurveyId: '1',
    CustomerId: '1',
    CustomerName: 'Test Customer',
    SurveyTypeId: '1',
    SurveyTypeName: 'Property Survey',
    StatusId: '1',
    Title: 'Test Survey 1',
    Description: 'Test Description 1',
    StartDate: '2024-01-01',
    EndDate: '2024-01-15',
    TotalCost: 1000,
    Notes: 'Test notes'
  },
  {
    SurveyId: '2',
    CustomerId: '2',
    CustomerName: 'Another Customer',
    SurveyTypeId: '2',
    SurveyTypeName: 'Boundary Survey',
    StatusId: '2',
    Title: 'Test Survey 2',
    Description: 'Test Description 2',
    StartDate: '2024-01-02',
    EndDate: '2024-01-16',
    TotalCost: 2000,
    Notes: 'Test notes 2'
  }
];

// Mock the GraphQL hooks module
jest.mock('../../hooks/useGraphQLApi', () => ({
  useSurveys: jest.fn(),
  useSurveyStatuses: jest.fn(),
  useCustomers: jest.fn(),
  useSurveyTypes: jest.fn(),
  useCreateSurvey: jest.fn(),
  useUpdateSurvey: jest.fn(),
  useDeleteSurvey: jest.fn(),
  useCreateSurveyStatus: jest.fn(),
  useUpdateSurveyStatus: jest.fn()
}));

// Test wrapper component
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

describe('Board Component - Comprehensive Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
    
    // Set up mock implementations
    (GraphQLApi.useSurveys as jest.Mock).mockReturnValue({
      data: {
        surveys: MOCK_SURVEYS,
        total: MOCK_SURVEYS.length
      },
      loading: false,
      error: null,
      refetch: jest.fn()
    });
    
    (GraphQLApi.useSurveyStatuses as jest.Mock).mockReturnValue({
      data: MOCK_SURVEY_STATUSES,
      loading: false,
      error: null,
      refetch: jest.fn()
    });
    
    (GraphQLApi.useCustomers as jest.Mock).mockReturnValue({
      data: MOCK_CUSTOMERS,
      loading: false,
      error: null,
      refetch: jest.fn()
    });
    
    (GraphQLApi.useSurveyTypes as jest.Mock).mockReturnValue({
      data: MOCK_SURVEY_TYPES,
      loading: false,
      error: null,
      refetch: jest.fn()
    });
    
    (GraphQLApi.useCreateSurvey as jest.Mock).mockReturnValue({
      create: jest.fn(),
      loading: false,
      error: null
    });
    
    (GraphQLApi.useUpdateSurvey as jest.Mock).mockReturnValue({
      update: jest.fn(),
      loading: false,
      error: null
    });
    
    (GraphQLApi.useDeleteSurvey as jest.Mock).mockReturnValue({
      delete: jest.fn(),
      loading: false,
      error: null
    });
    
    (GraphQLApi.useCreateSurveyStatus as jest.Mock).mockReturnValue({
      create: jest.fn(),
      loading: false,
      error: null
    });
    
    (GraphQLApi.useUpdateSurveyStatus as jest.Mock).mockReturnValue({
      update: jest.fn(),
      loading: false,
      error: null
    });
  });

  describe('Basic Rendering', () => {
    it('should render the board with title', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Survey Board')).toBeInTheDocument();
      });
    });

    it('should render status columns', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('New')).toBeInTheDocument();
        expect(screen.getByText('In Progress')).toBeInTheDocument();
        expect(screen.getByText('Complete')).toBeInTheDocument();
      }, { timeout: 3000 });
    });

    it('should render surveys in appropriate columns', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Test Survey 1')).toBeInTheDocument();
        expect(screen.getByText('Test Survey 2')).toBeInTheDocument();
      }, { timeout: 3000 });
    });
  });

  describe('Survey Card Content', () => {
    it('should display survey details correctly', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Test Survey 1')).toBeInTheDocument();
        expect(screen.getByText('Test Customer')).toBeInTheDocument();
        expect(screen.getByText('Property Survey')).toBeInTheDocument();
        expect(screen.getByText('$1,000')).toBeInTheDocument();
      });
    });

    it('should show survey dates', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('2024-01-01')).toBeInTheDocument();
        expect(screen.getByText('2024-01-15')).toBeInTheDocument();
      });
    });
  });

  describe('Column Management', () => {
    it('should render column management button', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const manageButton = screen.getByText('Manage Columns');
        expect(manageButton).toBeInTheDocument();
      });
    });

    it('should open column management modal when clicked', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const manageButton = screen.getByText('Manage Columns');
        fireEvent.click(manageButton);
      });

      await waitFor(() => {
        expect(screen.getByText('Manage Survey Status Columns')).toBeInTheDocument();
      });
    });

    it('should display status list in management modal', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const manageButton = screen.getByText('Manage Columns');
        fireEvent.click(manageButton);
      });

      await waitFor(() => {
        // Check that statuses are listed in the modal
        const modalContent = screen.getByText('Manage Survey Status Columns').closest('.fixed');
        expect(modalContent).toContainHTML('New');
        expect(modalContent).toContainHTML('In Progress');
        expect(modalContent).toContainHTML('Complete');
      });
    });
  });

  describe('Survey Actions', () => {
    it('should render add survey button', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const addButton = screen.getByText('Add Survey');
        expect(addButton).toBeInTheDocument();
      });
    });

    it('should open create survey modal when add button clicked', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const addButton = screen.getByText('Add Survey');
        fireEvent.click(addButton);
      });

      await waitFor(() => {
        expect(screen.getByText('Create New Survey')).toBeInTheDocument();
      });
    });

    it('should show survey edit options on hover/interaction', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const surveyCard = screen.getByText('Test Survey 1').closest('.bg-white');
        expect(surveyCard).toBeInTheDocument();
      });
    });
  });

  describe('LocalStorage Integration', () => {
    it('should attempt to load column order from localStorage', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(localStorageMock.getItem).toHaveBeenCalledWith('boardColumnOrder');
      });
    });

    it('should attempt to load hidden columns from localStorage', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(localStorageMock.getItem).toHaveBeenCalledWith('boardHiddenColumns');
      });
    });
  });

  describe('Accessibility', () => {
    it('should have proper heading structure', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const mainHeading = screen.getByRole('heading', { level: 1 });
        expect(mainHeading).toHaveTextContent('Survey Management Board');
      });
    });

    it('should have accessible buttons', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const addButton = screen.getByRole('button', { name: /add survey/i });
        expect(addButton).toBeInTheDocument();
        
        const manageButton = screen.getByRole('button', { name: /manage columns/i });
        expect(manageButton).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle empty survey data gracefully', async () => {
      // Mock empty data
      (GraphQLApi.useSurveys as jest.Mock).mockReturnValue({
        data: [],
        loading: false,
        error: null,
        refetch: jest.fn()
      });

      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Survey Management Board')).toBeInTheDocument();
        // Should still render columns even with no surveys
        expect(screen.getByText('New')).toBeInTheDocument();
      });
    });

    it('should handle localStorage errors gracefully', async () => {
      localStorageMock.getItem.mockImplementation(() => {
        throw new Error('localStorage error');
      });

      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Survey Management Board')).toBeInTheDocument();
      });
    });
  });

  describe('Loading States', () => {
    it('should handle loading state for surveys', async () => {
      (GraphQLApi.useSurveys as jest.Mock).mockReturnValue({
        data: null,
        loading: true,
        error: null,
        refetch: jest.fn()
      });

      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Survey Management Board')).toBeInTheDocument();
      });
    });
  });

  describe('Data Integration', () => {
    it('should group surveys by status correctly', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Survey 1 should be in "New" column (StatusId: '1')
        const newColumn = screen.getByText('New').closest('.flex-col');
        expect(newColumn).toContainHTML('Test Survey 1');
        
        // Survey 2 should be in "In Progress" column (StatusId: '2')
        const inProgressColumn = screen.getByText('In Progress').closest('.flex-col');
        expect(inProgressColumn).toContainHTML('Test Survey 2');
      });
    });

    it('should display survey count per column', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Should show count indicators
        expect(screen.getByText('1', { selector: '.bg-blue-100' })).toBeInTheDocument();
      });
    });
  });
});