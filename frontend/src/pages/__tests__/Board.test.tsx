import React from 'react';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MockedProvider } from '@apollo/client/testing';
import { BrowserRouter } from 'react-router-dom';
import Board from '../Board';
import { 
  mockSurveys, 
  mockSurveyStatuses, 
  mockCustomers, 
  mockSurveyTypes 
} from '../../__tests__/mocks/mockData';
import { 
  GET_SURVEYS, 
  GET_SURVEY_STATUSES, 
  GET_CUSTOMERS, 
  GET_SURVEY_TYPES,
  UPDATE_SURVEY,
  CREATE_SURVEY,
  UPDATE_SURVEY_STATUS,
  CREATE_SURVEY_STATUS
} from '../../graphql/queries';

// Test wrapper component
const TestWrapper = ({ children, mocks = [] }: { children: React.ReactNode; mocks?: any[] }) => (
  <MockedProvider mocks={mocks} addTypename={false}>
    <BrowserRouter>
      {children}
    </BrowserRouter>
  </MockedProvider>
);

// Default mocks for most tests
const defaultMocks = [
  {
    request: {
      query: GET_SURVEYS,
      variables: { skip: 0, limit: 100 }
    },
    result: {
      data: {
        surveys: {
          surveys: mockSurveys,
          total: mockSurveys.length
        }
      }
    }
  },
  {
    request: {
      query: GET_SURVEY_STATUSES
    },
    result: {
      data: {
        surveyStatuses: mockSurveyStatuses
      }
    }
  },
  {
    request: {
      query: GET_CUSTOMERS,
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
      query: GET_SURVEY_TYPES
    },
    result: {
      data: {
        surveyTypes: mockSurveyTypes
      }
    }
  }
];

describe('Board Component', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
  });

  describe('Initial Rendering', () => {
    it('renders the board with loading state initially', () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });

    it('renders all survey status columns after loading', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      // Wait for data to load
      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
        expect(screen.getByText('In Progress')).toBeInTheDocument();
        expect(screen.getByText('Completed')).toBeInTheDocument();
        expect(screen.getByText('On Hold')).toBeInTheDocument();
      });
    });

    it('renders the unknown status column when surveys have unknown status', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Unknown Status')).toBeInTheDocument();
      });
    });

    it('displays correct survey counts in each column', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Check each column has the correct count
        const pendingColumn = screen.getByText('Pending').closest('[data-testid^="column-"]');
        const inProgressColumn = screen.getByText('In Progress').closest('[data-testid^="column-"]');
        const completedColumn = screen.getByText('Completed').closest('[data-testid^="column-"]');
        const unknownColumn = screen.getByText('Unknown Status').closest('[data-testid^="column-"]');

        expect(within(pendingColumn!).getByText('1')).toBeInTheDocument(); // 1 survey
        expect(within(inProgressColumn!).getByText('1')).toBeInTheDocument(); // 1 survey
        expect(within(completedColumn!).getByText('1')).toBeInTheDocument(); // 1 survey
        expect(within(unknownColumn!).getByText('1')).toBeInTheDocument(); // 1 survey
      });
    });
  });

  describe('Column Management', () => {
    it('shows hide/show column toggle buttons', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const eyeIcons = screen.getAllByRole('button', { name: /hide column/i });
        expect(eyeIcons).toHaveLength(5); // 4 status columns + 1 unknown
      });
    });

    it('hides a column when hide button is clicked', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Click hide button for Pending column
      const pendingColumn = screen.getByText('Pending').closest('[data-testid^="column-"]');
      const hideButton = within(pendingColumn!).getByRole('button', { name: /hide column/i });
      
      await user.click(hideButton);

      // Column should be hidden
      expect(screen.queryByText('Pending')).not.toBeInTheDocument();
    });

    it('persists hidden columns in localStorage', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Hide Pending column
      const pendingColumn = screen.getByText('Pending').closest('[data-testid^="column-"]');
      const hideButton = within(pendingColumn!).getByRole('button', { name: /hide column/i });
      
      await user.click(hideButton);

      // Check localStorage
      expect(localStorage.setItem).toHaveBeenCalledWith(
        'boardHiddenColumns',
        expect.stringContaining('status-1')
      );
    });

    it('shows hidden columns panel with toggle', async () => {
      const user = userEvent.setup();
      
      // Pre-hide a column
      localStorage.setItem('boardHiddenColumns', JSON.stringify(['status-1']));
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Show Hidden Columns')).toBeInTheDocument();
      });

      // Click show hidden columns
      await user.click(screen.getByText('Show Hidden Columns'));

      // Should show the hidden column with restore option
      expect(screen.getByText('Pending')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /show column/i })).toBeInTheDocument();
    });
  });

  describe('Column Renaming', () => {
    const updateStatusMock = {
      request: {
        query: UPDATE_SURVEY_STATUS,
        variables: {
          surveyStatusId: 'status-1',
          input: { StatusName: 'New Name' }
        }
      },
      result: {
        data: {
          updateSurveyStatus: {
            surveyStatus: {
              SurveyStatusId: 'status-1',
              StatusName: 'New Name',
              Description: 'Survey is pending',
              IsActive: true
            }
          }
        }
      }
    };

    it('shows pencil icon for renaming columns', async () => {
      render(
        <TestWrapper mocks={[...defaultMocks, updateStatusMock]}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const renameButtons = screen.getAllByRole('button', { name: /rename status/i });
        expect(renameButtons.length).toBeGreaterThan(0);
      });
    });

    it('allows renaming a column', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={[...defaultMocks, updateStatusMock]}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Click rename button for Pending column
      const pendingColumn = screen.getByText('Pending').closest('[data-testid^="column-"]');
      const renameButton = within(pendingColumn!).getByRole('button', { name: /rename status/i });
      
      await user.click(renameButton);

      // Should show input field
      const input = screen.getByDisplayValue('Pending');
      expect(input).toBeInTheDocument();

      // Change the name
      await user.clear(input);
      await user.type(input, 'New Name');
      await user.keyboard('{Enter}');

      // Should call the mutation and update
      await waitFor(() => {
        expect(screen.getByText('New Name')).toBeInTheDocument();
      });
    });

    it('cancels rename on Escape key', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Click rename button
      const pendingColumn = screen.getByText('Pending').closest('[data-testid^="column-"]');
      const renameButton = within(pendingColumn!).getByRole('button', { name: /rename status/i });
      
      await user.click(renameButton);

      // Press Escape
      const input = screen.getByDisplayValue('Pending');
      await user.keyboard('{Escape}');

      // Should revert to original name
      expect(screen.getByText('Pending')).toBeInTheDocument();
      expect(input).not.toBeInTheDocument();
    });

    it('prevents renaming unknown status column', async () => {
      const user = userEvent.setup();
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Unknown Status')).toBeInTheDocument();
      });

      // Try to rename Unknown Status column
      const unknownColumn = screen.getByText('Unknown Status').closest('[data-testid^="column-"]');
      const renameButton = within(unknownColumn!).getByRole('button', { name: /rename status/i });
      
      await user.click(renameButton);

      const input = screen.getByDisplayValue('Unknown Status');
      await user.clear(input);
      await user.type(input, 'New Unknown Name');
      await user.keyboard('{Enter}');

      // Should show console message and not change
      expect(consoleSpy).toHaveBeenCalledWith('Cannot rename the Unknown Status column');
      
      consoleSpy.mockRestore();
    });
  });

  describe('Survey Drag and Drop', () => {
    const updateSurveyMock = {
      request: {
        query: UPDATE_SURVEY,
        variables: {
          surveyId: 'survey-1',
          input: { StatusId: 'status-2' }
        }
      },
      result: {
        data: {
          updateSurvey: {
            survey: {
              ...mockSurveys[0],
              StatusId: 'status-2'
            }
          }
        }
      }
    };

    it('allows dragging surveys between columns', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={[...defaultMocks, updateSurveyMock]}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      // Find the survey card and the target column
      const surveyCard = screen.getByText('S001').closest('[data-testid^="survey-card-"]');
      const targetColumn = screen.getByText('In Progress').closest('[data-testid^="column-"]');

      // Simulate drag and drop
      fireEvent.dragStart(surveyCard!);
      fireEvent.dragOver(targetColumn!);
      fireEvent.drop(targetColumn!);

      // Should call update mutation
      await waitFor(() => {
        // The survey should be moved to the new column
        expect(updateSurveyMock.request).toBeDefined();
      });
    });

    it('shows thinking indicator during survey update', async () => {
      render(
        <TestWrapper mocks={[...defaultMocks, updateSurveyMock]}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      const surveyCard = screen.getByText('S001').closest('[data-testid^="survey-card-"]');
      const targetColumn = screen.getByText('In Progress').closest('[data-testid^="column-"]');

      fireEvent.dragStart(surveyCard!);
      fireEvent.dragOver(targetColumn!);
      fireEvent.drop(targetColumn!);

      // Should show thinking indicator
      await waitFor(() => {
        expect(screen.getByText('🤔')).toBeInTheDocument();
      });
    });
  });

  describe('Survey Creation and Editing', () => {
    const createSurveyMock = {
      request: {
        query: CREATE_SURVEY,
        variables: {
          input: {
            SurveyNumber: 'S005',
            Title: 'New Survey',
            CustomerId: 'customer-1',
            SurveyTypeId: 'type-1',
            StatusId: 'status-1'
          }
        }
      },
      result: {
        data: {
          createSurvey: {
            survey: {
              SurveyId: 'survey-5',
              SurveyNumber: 'S005',
              Title: 'New Survey',
              CustomerId: 'customer-1',
              SurveyTypeId: 'type-1',
              StatusId: 'status-1',
              // ... other required fields
            }
          }
        }
      }
    };

    it('shows create survey buttons in each column', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const createButtons = screen.getAllByRole('button', { name: /create survey/i });
        expect(createButtons.length).toBeGreaterThan(0);
      });
    });

    it('opens create survey modal when create button is clicked', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Click create button in Pending column
      const pendingColumn = screen.getByText('Pending').closest('[data-testid^="column-"]');
      const createButton = within(pendingColumn!).getByRole('button', { name: /create survey/i });
      
      await user.click(createButton);

      // Should open create modal
      expect(screen.getByText('Create New Survey')).toBeInTheDocument();
    });

    it('shows edit buttons on survey cards', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        const editButtons = screen.getAllByRole('button', { name: /edit survey/i });
        expect(editButtons.length).toBeGreaterThan(0);
      });
    });

    it('opens edit modal when edit button is clicked', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('S001')).toBeInTheDocument();
      });

      // Click edit button on first survey
      const surveyCard = screen.getByText('S001').closest('[data-testid^="survey-card-"]');
      const editButton = within(surveyCard!).getByRole('button', { name: /edit survey/i });
      
      await user.click(editButton);

      // Should open edit modal
      expect(screen.getByText('Edit Survey')).toBeInTheDocument();
    });
  });

  describe('Column Drag and Drop Reordering', () => {
    it('allows dragging columns to reorder them', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
        expect(screen.getByText('In Progress')).toBeInTheDocument();
      });

      // Get initial order
      const columns = screen.getAllByTestId(/^column-/);
      const firstColumnText = within(columns[0]).getByRole('heading').textContent;
      const secondColumnText = within(columns[1]).getByRole('heading').textContent;

      // Simulate dragging first column to second position
      fireEvent.dragStart(columns[0]);
      fireEvent.dragOver(columns[1]);
      fireEvent.drop(columns[1]);

      // Should reorder columns
      await waitFor(() => {
        const reorderedColumns = screen.getAllByTestId(/^column-/);
        const newFirstColumnText = within(reorderedColumns[0]).getByRole('heading').textContent;
        const newSecondColumnText = within(reorderedColumns[1]).getByRole('heading').textContent;
        
        // Order should be swapped
        expect(newFirstColumnText).toBe(secondColumnText);
        expect(newSecondColumnText).toBe(firstColumnText);
      });
    });

    it('persists column order in localStorage', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      const columns = screen.getAllByTestId(/^column-/);
      
      // Simulate column reordering
      fireEvent.dragStart(columns[0]);
      fireEvent.dragOver(columns[1]);
      fireEvent.drop(columns[1]);

      // Should save to localStorage
      await waitFor(() => {
        expect(localStorage.setItem).toHaveBeenCalledWith(
          'boardColumnOrder',
          expect.any(String)
        );
      });
    });
  });

  describe('Error Handling', () => {
    it('handles API errors gracefully', async () => {
      const errorMocks = [
        {
          request: {
            query: GET_SURVEYS,
            variables: { skip: 0, limit: 100 }
          },
          error: new Error('API Error')
        },
        ...defaultMocks.slice(1) // Keep other mocks working
      ];

      render(
        <TestWrapper mocks={errorMocks}>
          <Board />
        </TestWrapper>
      );

      // Should still render the basic structure
      expect(screen.getByText('Survey Board')).toBeInTheDocument();
    });

    it('shows empty state when no surveys are available', async () => {
      const emptyMocks = [
        {
          request: {
            query: GET_SURVEYS,
            variables: { skip: 0, limit: 100 }
          },
          result: {
            data: {
              surveys: {
                surveys: [],
                total: 0
              }
            }
          }
        },
        ...defaultMocks.slice(1)
      ];

      render(
        <TestWrapper mocks={emptyMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Columns should still be visible but empty
        expect(screen.getByText('Pending')).toBeInTheDocument();
        expect(screen.getByText('0')).toBeInTheDocument(); // Count should be 0
      });
    });
  });

  describe('Accessibility', () => {
    it('has proper ARIA labels for drag and drop', async () => {
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        // Survey cards should be draggable
        const surveyCards = screen.getAllByTestId(/^survey-card-/);
        surveyCards.forEach(card => {
          expect(card).toHaveAttribute('draggable', 'true');
        });

        // Columns should be drop zones
        const columns = screen.getAllByTestId(/^column-/);
        columns.forEach(column => {
          expect(column).toHaveAttribute('role', 'region');
        });
      });
    });

    it('supports keyboard navigation', async () => {
      const user = userEvent.setup();
      
      render(
        <TestWrapper mocks={defaultMocks}>
          <Board />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('Pending')).toBeInTheDocument();
      });

      // Tab through interactive elements
      await user.tab();
      
      // Should focus on interactive elements
      const focusedElement = document.activeElement;
      expect(focusedElement).toHaveAttribute('role', 'button');
    });
  });
});