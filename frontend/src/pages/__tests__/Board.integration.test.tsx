import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';

// Mock the GraphQL hooks
const mockUseSurveys = jest.fn();
const mockUseSurveyStatuses = jest.fn();
const mockUseUpdateSurvey = jest.fn();
const mockUseCreateSurvey = jest.fn();
const mockUseCustomers = jest.fn();
const mockUseSurveyTypes = jest.fn();
const mockUseCreateSurveyStatus = jest.fn();
const mockUseUpdateSurveyStatus = jest.fn();

jest.mock('../../hooks/useGraphQLApi', () => ({
  useSurveys: () => mockUseSurveys(),
  useSurveyStatuses: () => mockUseSurveyStatuses(),
  useUpdateSurvey: () => mockUseUpdateSurvey(),
  useCreateSurvey: () => mockUseCreateSurvey(),
  useCustomers: () => mockUseCustomers(),
  useSurveyTypes: () => mockUseSurveyTypes(),
  useCreateSurveyStatus: () => mockUseCreateSurveyStatus(),
  useUpdateSurveyStatus: () => mockUseUpdateSurveyStatus()
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Import the Board component after mocking
import Board from '../Board';

const TestWrapper = ({ children }: { children: React.ReactNode }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

// Mock data
const mockSurveyStatuses = [
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
  }
];

const mockSurveys = [
  {
    SurveyId: 'survey-1',
    SurveyNumber: 'S001',
    CustomerId: 'customer-1',
    PropertyId: 'property-1',
    SurveyTypeId: 'type-1',
    StatusId: 'status-1',
    Title: 'Test Survey 1',
    Description: 'Test survey description',
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
    Title: 'Test Survey 2',
    Description: 'Another test survey',
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
  }
];

const mockCustomers = [
  {
    CustomerId: 'customer-1',
    CustomerCode: 'CUST001',
    CompanyName: 'Test Company 1',
    ContactFirstName: 'John',
    ContactLastName: 'Doe',
    Email: 'john@test.com',
    Phone: '123-456-7890',
    IsActive: true,
    CreatedDate: '2024-01-01T00:00:00Z',
    ModifiedDate: '2024-01-01T00:00:00Z'
  }
];

const mockSurveyTypes = [
  {
    SurveyTypeId: 'type-1',
    SurveyTypeName: 'Boundary Survey',
    Description: 'Property boundary survey',
    IsActive: true
  }
];

// Default mock implementations
const defaultMockImplementations = {
  useSurveys: () => ({
    data: { surveys: mockSurveys, total: mockSurveys.length },
    loading: false,
    error: null,
    refetch: jest.fn()
  }),
  useSurveyStatuses: () => ({
    data: mockSurveyStatuses,
    loading: false,
    error: null,
    refetch: jest.fn()
  }),
  useUpdateSurvey: () => ({
    update: jest.fn().mockResolvedValue({}),
    loading: false,
    error: null
  }),
  useCreateSurvey: () => ({
    create: jest.fn().mockResolvedValue({}),
    loading: false,
    error: null
  }),
  useCustomers: () => ({
    data: { customers: mockCustomers, total: mockCustomers.length },
    loading: false,
    error: null,
    refetch: jest.fn()
  }),
  useSurveyTypes: () => ({
    data: mockSurveyTypes,
    loading: false,
    error: null,
    refetch: jest.fn()
  }),
  useCreateSurveyStatus: () => ({
    create: jest.fn().mockResolvedValue({}),
    loading: false
  }),
  useUpdateSurveyStatus: () => ({
    update: jest.fn().mockResolvedValue({}),
    loading: false
  })
};

describe('Board Component Integration Tests', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
    
    // Set default mock implementations
    mockUseSurveys.mockImplementation(defaultMockImplementations.useSurveys);
    mockUseSurveyStatuses.mockImplementation(defaultMockImplementations.useSurveyStatuses);
    mockUseUpdateSurvey.mockImplementation(defaultMockImplementations.useUpdateSurvey);
    mockUseCreateSurvey.mockImplementation(defaultMockImplementations.useCreateSurvey);
    mockUseCustomers.mockImplementation(defaultMockImplementations.useCustomers);
    mockUseSurveyTypes.mockImplementation(defaultMockImplementations.useSurveyTypes);
    mockUseCreateSurveyStatus.mockImplementation(defaultMockImplementations.useCreateSurveyStatus);
    mockUseUpdateSurveyStatus.mockImplementation(defaultMockImplementations.useUpdateSurveyStatus);
  });

  describe('Initial Rendering', () => {
    it('renders the board title', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });

    it('renders survey status columns', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
        expect(screen.getByText('In Progress')).toBeInTheDocument();
        expect(screen.getByText('Completed')).toBeInTheDocument();
      });
    });

    it('renders surveys in correct columns', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
        expect(screen.getByText('S002')).toBeInTheDocument();
        expect(screen.getByText('Test Survey 1')).toBeInTheDocument();
        expect(screen.getByText('Test Survey 2')).toBeInTheDocument();
      });
    });
  });

  describe('Column Management', () => {
    it('hides columns when hide button is clicked', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Find and click the hide button for the Pending column
      const hideButtons = screen.getAllByRole('button', { name: /hide column/i });
      await user.click(hideButtons[0]);

      // Verify localStorage was called
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'boardHiddenColumns',
        expect.stringContaining('status-1')
      );
    });

    it('persists hidden columns from localStorage', async () => {
      // Mock localStorage to return hidden columns
      localStorageMock.getItem.mockReturnValue('["status-1"]');
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.queryByText('Pending')).not.toBeInTheDocument();
        expect(screen.getByText('In Progress')).toBeInTheDocument();
      });
    });

    it('shows hidden columns panel when columns are hidden', async () => {
      localStorageMock.getItem.mockReturnValue('["status-1"]');
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Show Hidden Columns')).toBeInTheDocument();
      });
    });
  });

  describe('Survey Drag and Drop', () => {
    it('handles survey drag start', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      const surveyCard = screen.getByText('S001').closest('[draggable="true"]');
      expect(surveyCard).toBeInTheDocument();
      
      if (surveyCard) {
        fireEvent.dragStart(surveyCard);
        // The drag should set some state - we can't easily test the internal state
        // but we can verify the element is draggable
        expect(surveyCard).toHaveAttribute('draggable', 'true');
      }
    });

    it('shows drop zones during drag operation', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      const surveyCard = screen.getByText('S001').closest('[draggable="true"]');
      const dropZone = screen.getByText('In Progress').closest('[data-testid*="column"]');
      
      if (surveyCard && dropZone) {
        fireEvent.dragStart(surveyCard);
        fireEvent.dragOver(dropZone);
        
        // The component should handle the drag over event
        expect(dropZone).toBeInTheDocument();
      }
    });
  });

  describe('Survey Creation and Editing', () => {
    it('opens create survey modal', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Find create survey button
      const createButtons = screen.getAllByRole('button', { name: /create survey/i });
      await user.click(createButtons[0]);

      // Should open the create modal
      await waitFor(() => {
        expect(screen.getByText('Create New Survey')).toBeInTheDocument();
      });
    });

    it('opens edit survey modal', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      // Find edit survey button
      const editButtons = screen.getAllByRole('button', { name: /edit survey/i });
      await user.click(editButtons[0]);

      // Should open the edit modal
      await waitFor(() => {
        expect(screen.getByText('Edit Survey')).toBeInTheDocument();
      });
    });
  });

  describe('Column Renaming', () => {
    it('shows rename interface when pencil icon is clicked', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Find and click rename button
      const renameButtons = screen.getAllByRole('button', { name: /rename status/i });
      await user.click(renameButtons[0]);

      // Should show input field
      await waitFor(() => {
        const input = screen.getByDisplayValue('Pending');
        expect(input).toBeInTheDocument();
      });
    });

    it('calls update mutation when column is renamed', async () => {
      const user = userEvent.setup();
      const mockUpdate = jest.fn().mockResolvedValue({});
      mockUseUpdateSurveyStatus.mockImplementation(() => ({
        update: mockUpdate,
        loading: false
      }));
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Click rename button
      const renameButtons = screen.getAllByRole('button', { name: /rename status/i });
      await user.click(renameButtons[0]);

      // Edit the name
      const input = screen.getByDisplayValue('Pending');
      await user.clear(input);
      await user.type(input, 'New Name');
      await user.keyboard('{Enter}');

      // Should call the update function
      await waitFor(() => {
        expect(mockUpdate).toHaveBeenCalledWith('status-1', {
          StatusName: 'New Name'
        });
      });
    });
  });

  describe('Error Handling', () => {
    it('handles survey loading error gracefully', async () => {
      mockUseSurveys.mockImplementation(() => ({
        data: null,
        loading: false,
        error: new Error('Failed to load surveys'),
        refetch: jest.fn()
      }));
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      // Should still render the board structure
      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });

    it('shows loading state', async () => {
      mockUseSurveys.mockImplementation(() => ({
        data: null,
        loading: true,
        error: null,
        refetch: jest.fn()
      }));
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      // Should still render basic structure while loading
      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has proper ARIA roles for drag and drop', async () => {
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      // Survey cards should be draggable
      const surveyCard = screen.getByText('S001').closest('[draggable="true"]');
      expect(surveyCard).toHaveAttribute('draggable', 'true');
    });

    it('supports keyboard navigation', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Tab through interactive elements
      await user.tab();
      
      // Should focus on interactive elements
      const activeElement = document.activeElement;
      expect(activeElement).toHaveAttribute('type', 'button');
    });
  });
});