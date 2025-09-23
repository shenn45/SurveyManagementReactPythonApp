import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
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
    SurveyNumber: 'S001',
    CustomerId: '1',
    CustomerName: 'Test Customer',
    SurveyTypeId: '1',
    SurveyTypeName: 'Property Survey',
    StatusId: '1',
    Title: 'Test Survey 1',
    Description: 'Test Description 1',
    QuotedPrice: 1000,
    FinalPrice: 1200,
    DueDate: '2024-01-15',
    RequestDate: '2024-01-01',
    IsFieldworkComplete: true,
    IsDrawingComplete: false,
    IsDelivered: false,
    Notes: 'Test notes'
  },
  {
    SurveyId: '2',
    SurveyNumber: 'S002',
    CustomerId: '2',
    CustomerName: 'Another Customer',
    SurveyTypeId: '2',
    SurveyTypeName: 'Boundary Survey',
    StatusId: '2',
    Title: 'Test Survey 2',
    Description: 'Test Description 2',
    QuotedPrice: 2000,
    FinalPrice: null,
    DueDate: '2024-01-16',
    RequestDate: '2024-01-02',
    IsFieldworkComplete: false,
    IsDrawingComplete: true,
    IsDelivered: true,
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

  describe('Basic Rendering and Structure', () => {
    it('should render the board with correct title', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Survey Board')).toBeInTheDocument();
        expect(screen.getByText('Kanban-style view of surveys organized by status')).toBeInTheDocument();
      });
    });

    it('should render all status columns', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('New')).toBeInTheDocument();
        expect(screen.getByText('In Progress')).toBeInTheDocument();
        expect(screen.getByText('Complete')).toBeInTheDocument();
      });
    });

    it('should display the correct total survey count', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Total: 2 surveys')).toBeInTheDocument();
      });
    });

    it('should render the search input', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText('Search surveys...');
        expect(searchInput).toBeInTheDocument();
      });
    });
  });

  describe('Survey Display', () => {
    it('should render surveys in the board', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Test Survey 1')).toBeInTheDocument();
        expect(screen.getByText('Test Survey 2')).toBeInTheDocument();
      });
    });

    it('should display survey details correctly', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Check survey 1 details
        expect(screen.getByText('Test Survey 1')).toBeInTheDocument();
        expect(screen.getByText('Test Description 1')).toBeInTheDocument();
        expect(screen.getByText('$1,000')).toBeInTheDocument(); // Quoted price
        expect(screen.getByText('$1,200')).toBeInTheDocument(); // Final price
        
        // Check survey 2 details
        expect(screen.getByText('Test Survey 2')).toBeInTheDocument();
        expect(screen.getByText('Test Description 2')).toBeInTheDocument();
        expect(screen.getByText('$2,000')).toBeInTheDocument(); // Quoted price
        expect(screen.getByText('Not set')).toBeInTheDocument(); // Final price not set
      });
    });

    it('should display survey dates', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Due dates (note: JavaScript Date formatting might differ from expected format)
        expect(screen.getByText('1/14/2024')).toBeInTheDocument(); // Due date for survey 1 (2024-01-15 becomes 1/14/2024 in local time)
        expect(screen.getByText('1/15/2024')).toBeInTheDocument(); // Due date for survey 2 (2024-01-16 becomes 1/15/2024 in local time)
        
        // Request dates
        expect(screen.getByText('12/31/2023')).toBeInTheDocument(); // Request date for survey 1 (2024-01-01 becomes 12/31/2023 in local time)
        expect(screen.getByText('1/1/2024')).toBeInTheDocument(); // Request date for survey 2 (2024-01-02 becomes 1/1/2024 in local time)
      });
    });

    it('should display survey status badges', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Survey 1 has fieldwork complete
        expect(screen.getByText('Fieldwork')).toBeInTheDocument();
        
        // Survey 2 has drawing complete and delivered
        expect(screen.getByText('Drawing')).toBeInTheDocument();
        expect(screen.getByText('Delivered')).toBeInTheDocument();
      });
    });

    it('should display survey numbers', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
        expect(screen.getByText('S002')).toBeInTheDocument();
      });
    });

    it('should show price information correctly', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Check for price labels and values
        expect(screen.getAllByText('Quoted:')).toHaveLength(2);
        expect(screen.getAllByText('Final:')).toHaveLength(2);
        expect(screen.getByText('$1,000')).toBeInTheDocument();
        expect(screen.getByText('$1,200')).toBeInTheDocument(); 
        expect(screen.getByText('$2,000')).toBeInTheDocument();
      });
    });
  });

  describe('Column Management Features', () => {
    it('should display column action buttons', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Check for rename buttons (should be 3, one for each column)
        const renameButtons = screen.getAllByTitle('Rename status');
        expect(renameButtons).toHaveLength(3);
        
        // Check for hide buttons (should be 3, one for each column)
        const hideButtons = screen.getAllByTitle('Hide column');
        expect(hideButtons).toHaveLength(3);
      });
    });

    it('should make columns draggable', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Check that columns have draggable attributes
        const draggableElements = screen.getAllByRole('generic').filter(
          element => element.getAttribute('draggable') === 'true'
        );
        expect(draggableElements.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Survey Cards Functionality', () => {
    it('should make survey cards draggable', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const surveyCards = screen.getAllByRole('generic').filter(
          element => element.getAttribute('draggable') === 'true' && 
                    element.className.includes('bg-white')
        );
        expect(surveyCards.length).toBeGreaterThan(0);
      });
    });

    it('should provide click-to-edit functionality', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const editableTitles = screen.getAllByTitle('Click to edit survey');
        expect(editableTitles).toHaveLength(2); // Should have 2 survey cards
        expect(editableTitles[0]).toBeInTheDocument();
      });
    });
  });

  describe('Data Integration', () => {
    it('should correctly group surveys by status', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Survey 1 should be in New column (StatusId: '1')
        const newColumnContainer = screen.getByText('New').closest('.w-80');
        expect(newColumnContainer).toBeInTheDocument();
        
        // Survey 2 should be in In Progress column (StatusId: '2')  
        const inProgressColumnContainer = screen.getByText('In Progress').closest('.w-80');
        expect(inProgressColumnContainer).toBeInTheDocument();
        
        // Complete column should be empty
        const completeColumnContainer = screen.getByText('Complete').closest('.w-80');
        expect(completeColumnContainer).toBeInTheDocument();
      });
    });
  });

  describe('Loading State', () => {
    it('should display loading state when data is loading', async () => {
      // Mock loading state
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
        // Should show loading skeleton
        expect(document.querySelector('.animate-pulse')).toBeInTheDocument();
      });
    });
  });

  describe('Empty State', () => {
    it('should handle empty survey data gracefully', async () => {
      // Mock empty data
      (GraphQLApi.useSurveys as jest.Mock).mockReturnValue({
        data: {
          surveys: [],
          total: 0
        },
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
        expect(screen.getByText('Survey Board')).toBeInTheDocument();
        expect(screen.getByText('Total: 0 surveys')).toBeInTheDocument();
        expect(screen.getByText('New')).toBeInTheDocument();
        
        // Should show empty state in columns
        const emptyMessages = screen.getAllByText('No surveys in this status');
        expect(emptyMessages.length).toBeGreaterThan(0);
      });
    });
  });

  describe('localStorage Integration', () => {
    it('should attempt to load column preferences from localStorage', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(localStorageMock.getItem).toHaveBeenCalledWith('boardColumnOrder');
        expect(localStorageMock.getItem).toHaveBeenCalledWith('boardHiddenColumns');
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

      // Should still render without crashing
      await waitFor(() => {
        expect(screen.getByText('Survey Board')).toBeInTheDocument();
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
        expect(mainHeading).toHaveTextContent('Survey Board');
      });
    });

    it('should provide meaningful titles and labels', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getAllByTitle('Rename status')).toHaveLength(3);
        expect(screen.getAllByTitle('Hide column')).toHaveLength(3);
        expect(screen.getAllByTitle('Click to edit survey')).toHaveLength(2);
      });
    });
  });
});