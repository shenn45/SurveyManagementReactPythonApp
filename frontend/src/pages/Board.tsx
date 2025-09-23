import React, { useState, useEffect } from 'react';
import { EyeIcon, EyeSlashIcon, AdjustmentsHorizontalIcon, XMarkIcon, PlusIcon, PencilIcon } from '@heroicons/react/24/outline';
import { useSurveys, useSurveyStatuses, useUpdateSurvey, useCreateSurvey, useCustomers, useSurveyTypes, useCreateSurveyStatus, useUpdateSurveyStatus } from '../hooks/useGraphQLApi';
import { Survey, SurveyStatus, SurveyCreate } from '../types';

interface SurveyCard {
  survey: Survey;
  onDragStart: (survey: Survey) => void;
  isUpdating?: boolean;
  onEdit: (survey: Survey) => void;
}

const SurveyCard: React.FC<SurveyCard> = ({ survey, onDragStart, isUpdating = false, onEdit }) => {
  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString();
  };

  const formatPrice = (price: number | null | undefined) => {
    if (price === null || price === undefined) return 'Not set';
    return `$${price.toLocaleString()}`;
  };

  return (
    <div 
      className={`bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-3 hover:shadow-md transition-all cursor-move relative ${
        isUpdating ? 'opacity-70' : ''
      }`}
      draggable={!isUpdating}
      onDragStart={() => !isUpdating && onDragStart(survey)}
    >
      {/* Loading overlay */}
      {isUpdating && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-lg z-10">
          <div className="flex items-center space-x-2 text-blue-600">
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="text-sm font-medium">Updating...</span>
          </div>
        </div>
      )}
      
      <div className="flex justify-between items-start mb-2">
        <h4 
          className="font-medium text-gray-900 truncate cursor-pointer hover:text-blue-600 transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            onEdit(survey);
          }}
          title="Click to edit survey"
        >
          {survey.Title || survey.SurveyNumber}
        </h4>
        <span className="text-xs text-gray-500 ml-2">{survey.SurveyNumber}</span>
      </div>
      
      {survey.Description && (
        <p className="text-sm text-gray-600 mb-3 overflow-hidden" style={{ 
          display: '-webkit-box', 
          WebkitLineClamp: 2, 
          WebkitBoxOrient: 'vertical' 
        }}>
          {survey.Description}
        </p>
      )}
      
      <div className="space-y-1 text-xs text-gray-500">
        <div className="flex justify-between">
          <span>Quoted:</span>
          <span className="font-medium">{formatPrice(survey.QuotedPrice)}</span>
        </div>
        <div className="flex justify-between">
          <span>Final:</span>
          <span className="font-medium">{formatPrice(survey.FinalPrice)}</span>
        </div>
        <div className="flex justify-between">
          <span>Due:</span>
          <span className="font-medium">{formatDate(survey.DueDate)}</span>
        </div>
      </div>
      
      <div className="flex justify-between items-center mt-3 pt-3 border-t border-gray-100">
        <div className="flex space-x-2">
          {survey.IsFieldworkComplete && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
              Fieldwork
            </span>
          )}
          {survey.IsDrawingComplete && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
              Drawing
            </span>
          )}
          {survey.IsDelivered && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
              Delivered
            </span>
          )}
        </div>
        <span className="text-xs text-gray-400">
          {formatDate(survey.RequestDate)}
        </span>
      </div>
    </div>
  );
};

interface BoardColumn {
  status: SurveyStatus;
  surveys: Survey[];
  onHide: (statusId: string) => void;
  onDragStart: (survey: Survey) => void;
  onDragOver: (e: React.DragEvent) => void;
  onDrop: (e: React.DragEvent, targetStatusId: string) => void;
  isDragOver: boolean;
  updatingSurveyId?: string | null;
  onCreateSurvey: (statusId: string) => void;
  onEdit: (survey: Survey) => void;
  onRenameStatus: (newName: string) => void;
  editingStatus: SurveyStatus | null;
  setEditingStatus: React.Dispatch<React.SetStateAction<SurveyStatus | null>>;
}

const BoardColumn: React.FC<BoardColumn> = ({ 
  status, 
  surveys, 
  onHide, 
  onDragStart, 
  onDragOver, 
  onDrop,
  isDragOver,
  updatingSurveyId,
  onCreateSurvey,
  onEdit,
  onRenameStatus,
  editingStatus,
  setEditingStatus
}) => {
  const getColumnColor = (statusName: string) => {
    const name = statusName.toLowerCase();
    if (name.includes('pending') || name.includes('new')) return 'bg-yellow-50 border-yellow-200';
    if (name.includes('progress') || name.includes('active')) return 'bg-blue-50 border-blue-200';
    if (name.includes('review') || name.includes('approval')) return 'bg-orange-50 border-orange-200';
    if (name.includes('complete') || name.includes('finished')) return 'bg-green-50 border-green-200';
    if (name.includes('cancelled') || name.includes('rejected')) return 'bg-red-50 border-red-200';
    return 'bg-gray-50 border-gray-200';
  };

  const getHeaderColor = (statusName: string) => {
    const name = statusName.toLowerCase();
    if (name.includes('pending') || name.includes('new')) return 'text-yellow-800 bg-yellow-100';
    if (name.includes('progress') || name.includes('active')) return 'text-blue-800 bg-blue-100';
    if (name.includes('review') || name.includes('approval')) return 'text-orange-800 bg-orange-100';
    if (name.includes('complete') || name.includes('finished')) return 'text-green-800 bg-green-100';
    if (name.includes('cancelled') || name.includes('rejected')) return 'text-red-800 bg-red-100';
    return 'text-gray-800 bg-gray-100';
  };

  return (
    <div 
      className={`flex-shrink-0 w-80 ${getColumnColor(status.StatusName)} border-2 rounded-lg transition-colors ${
        isDragOver ? 'ring-2 ring-indigo-500 ring-opacity-50 bg-indigo-50' : ''
      }`}
      onDragOver={onDragOver}
      onDrop={(e) => onDrop(e, status.SurveyStatusId)}
    >
      <div className={`p-4 border-b border-gray-200`}>
        <div className="flex justify-between items-center">
          {editingStatus?.SurveyStatusId === status.SurveyStatusId ? (
            <input
              type="text"
              defaultValue={status.StatusName}
              autoFocus
              onBlur={(e) => {
                onRenameStatus(e.target.value);
              }}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  onRenameStatus((e.target as HTMLInputElement).value);
                }
                if (e.key === 'Escape') {
                  setEditingStatus(null);
                }
              }}
              className="font-semibold text-sm px-3 py-1 rounded-full bg-white border-2 border-blue-500 focus:outline-none"
            />
          ) : (
            <div className="flex items-center space-x-2">
              <h3 className={`font-semibold text-sm px-3 py-1 rounded-full ${getHeaderColor(status.StatusName)}`}>
                {status.StatusName}
              </h3>
              <button
                onClick={() => setEditingStatus(status)}
                className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                title="Rename status"
              >
                <PencilIcon className="h-4 w-4" />
              </button>
            </div>
          )}
          <div className="flex items-center space-x-2">
            <span className="bg-white text-gray-600 text-xs px-2 py-1 rounded-full font-medium">
              {surveys.length}
            </span>
            <button
              onClick={() => onHide(status.SurveyStatusId)}
              className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
              title="Hide column"
            >
              <EyeSlashIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
        {status.Description && (
          <p className="text-xs text-gray-600 mt-2">{status.Description}</p>
        )}
      </div>
      
      <div 
        className="p-4 max-h-screen overflow-y-auto cursor-pointer"
        onClick={(e) => {
          // Only trigger if clicking on empty space (not on survey cards)
          if (e.target === e.currentTarget) {
            onCreateSurvey(status.SurveyStatusId);
          }
        }}
      >
        {surveys.length === 0 ? (
          <div className="text-center py-8 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
            <p className="text-sm">No surveys in this status</p>
            <p className="text-xs mt-1">Drop surveys here to update status</p>
            <p className="text-xs mt-2 text-blue-500">Click to create new survey</p>
          </div>
        ) : (
          <>
            {surveys.map((survey) => (
              <SurveyCard 
                key={survey.SurveyId} 
                survey={survey} 
                onDragStart={onDragStart}
                isUpdating={updatingSurveyId === survey.SurveyId}
                onEdit={onEdit}
              />
            ))}
            {/* Add new survey button at bottom of column */}
            <div 
              className="mt-3 p-3 border-2 border-dashed border-gray-300 rounded-lg text-center text-gray-400 hover:border-blue-400 hover:text-blue-500 hover:bg-blue-50 transition-colors cursor-pointer"
              onClick={(e) => {
                e.stopPropagation();
                onCreateSurvey(status.SurveyStatusId);
              }}
            >
              <p className="text-sm">+ Add new survey</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default function Board() {
  const [searchTerm, setSearchTerm] = useState('');
  const [hiddenColumns, setHiddenColumns] = useState<Set<string>>(() => {
    // Load hidden columns from localStorage on initial render
    try {
      const saved = localStorage.getItem('boardHiddenColumns');
      return saved ? new Set(JSON.parse(saved)) : new Set();
    } catch (error) {
      console.warn('Failed to load hidden columns from localStorage:', error);
      return new Set();
    }
  });
  const [draggedSurvey, setDraggedSurvey] = useState<Survey | null>(null);
  const [dragOverColumn, setDragOverColumn] = useState<string | null>(null);
  const [updatingSurveyId, setUpdatingSurveyId] = useState<string | null>(null);
  
  // Modal state
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isColumnManagementOpen, setIsColumnManagementOpen] = useState(false);
  const [editingSurvey, setEditingSurvey] = useState<Survey | null>(null);
  const [prefilledStatusId, setPrefilledStatusId] = useState<string | null>(null);
  
  // Column management state
  const [columnOrder, setColumnOrder] = useState<string[]>([]);
  const [editingStatus, setEditingStatus] = useState<SurveyStatus | null>(null);
  const [newStatusName, setNewStatusName] = useState('');
  const [draggedColumn, setDraggedColumn] = useState<string | null>(null);
  const [formData, setFormData] = useState<SurveyCreate>({
    SurveyNumber: '',
    CustomerId: undefined,
    PropertyId: undefined,
    SurveyTypeId: undefined,
    StatusId: undefined,
    Title: '',
    Description: '',
    PurposeCode: '',
    RequestDate: '',
    ScheduledDate: '',
    DueDate: '',
    QuotedPrice: 0,
    FinalPrice: 0,
    IsFieldworkComplete: false,
    IsDrawingComplete: false,
    IsScanned: false,
    IsDelivered: false,
  });
  
  // Fetch all surveys (we'll handle filtering on frontend for board view)
  const { data: surveysData, loading: surveysLoading, error: surveysError, refetch } = useSurveys(1, 1000, searchTerm || undefined);
  const { data: statusesData, loading: statusesLoading, refetch: refetchStatuses } = useSurveyStatuses();
  const { update: updateSurvey, loading: updateLoading } = useUpdateSurvey();
  const { create: createSurvey, loading: createLoading } = useCreateSurvey();
  const { data: customersData } = useCustomers(1, 1000);
  const { data: surveyTypesData } = useSurveyTypes();
  const { create: createSurveyStatus, loading: createStatusLoading } = useCreateSurveyStatus();
  const { update: updateSurveyStatus } = useUpdateSurveyStatus();

  const [groupedSurveys, setGroupedSurveys] = useState<{ [key: string]: Survey[] }>({});

  // Save hidden columns to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem('boardHiddenColumns', JSON.stringify(Array.from(hiddenColumns)));
    } catch (error) {
      console.warn('Failed to save hidden columns to localStorage:', error);
    }
  }, [hiddenColumns]);

  // Initialize and save column order
  useEffect(() => {
    if (statusesData && statusesData.length > 0) {
      try {
        const saved = localStorage.getItem('boardColumnOrder');
        if (saved) {
          const savedOrder = JSON.parse(saved);
          // Filter to only include statuses that still exist
          const validOrder = savedOrder.filter((id: string) => 
            statusesData.some(status => status.SurveyStatusId === id)
          );
          // Add any new statuses that aren't in the saved order
          const newStatuses = statusesData
            .filter(status => !validOrder.includes(status.SurveyStatusId))
            .map(status => status.SurveyStatusId);
          setColumnOrder([...validOrder, ...newStatuses]);
        } else {
          // First time - use default order
          setColumnOrder(statusesData.map(status => status.SurveyStatusId));
        }
      } catch (error) {
        console.warn('Failed to load column order from localStorage:', error);
        setColumnOrder(statusesData.map(status => status.SurveyStatusId));
      }
    }
  }, [statusesData]);

  // Save column order to localStorage whenever it changes
  useEffect(() => {
    if (columnOrder.length > 0) {
      try {
        localStorage.setItem('boardColumnOrder', JSON.stringify(columnOrder));
      } catch (error) {
        console.warn('Failed to save column order to localStorage:', error);
      }
    }
  }, [columnOrder]);

  useEffect(() => {
    if (surveysData?.surveys && statusesData) {
      // Group surveys by their status
      const grouped = surveysData.surveys.reduce((acc, survey) => {
        const statusId = survey.StatusId || 'unknown';
        if (!acc[statusId]) {
          acc[statusId] = [];
        }
        acc[statusId].push(survey);
        return acc;
      }, {} as { [key: string]: Survey[] });

      setGroupedSurveys(grouped);
    }
  }, [surveysData, statusesData]);

  const handleHideColumn = (statusId: string) => {
    setHiddenColumns(prev => {
      const newSet = new Set(prev);
      newSet.add(statusId);
      return newSet;
    });
  };

  const handleShowColumn = (statusId: string) => {
    setHiddenColumns(prev => {
      const newSet = new Set(prev);
      newSet.delete(statusId);
      return newSet;
    });
  };

  const handleShowAllColumns = () => {
    setHiddenColumns(new Set());
    // This will trigger the useEffect above to save to localStorage
  };

  // Create survey handler
  const handleCreateSurvey = (statusId: string) => {
    setPrefilledStatusId(statusId);
    setFormData(prev => ({ ...prev, StatusId: statusId }));
    setIsCreateModalOpen(true);
  };

  // Edit survey handler
  const handleEditSurvey = (survey: Survey) => {
    setEditingSurvey(survey);
    setFormData({
      SurveyNumber: survey.SurveyNumber,
      CustomerId: survey.CustomerId,
      PropertyId: survey.PropertyId,
      SurveyTypeId: survey.SurveyTypeId,
      StatusId: survey.StatusId,
      Title: survey.Title || '',
      Description: survey.Description || '',
      PurposeCode: survey.PurposeCode || '',
      RequestDate: survey.RequestDate || '',
      ScheduledDate: survey.ScheduledDate || '',
      DueDate: survey.DueDate || '',
      QuotedPrice: survey.QuotedPrice || 0,
      FinalPrice: survey.FinalPrice || 0,
      IsFieldworkComplete: survey.IsFieldworkComplete,
      IsDrawingComplete: survey.IsDrawingComplete,
      IsScanned: survey.IsScanned,
      IsDelivered: survey.IsDelivered,
    });
    setIsEditModalOpen(true);
  };

  // Modal handlers
  const resetForm = () => {
    setFormData({
      SurveyNumber: '',
      CustomerId: undefined,
      PropertyId: undefined,
      SurveyTypeId: undefined,
      StatusId: prefilledStatusId || undefined,
      Title: '',
      Description: '',
      PurposeCode: '',
      RequestDate: '',
      ScheduledDate: '',
      DueDate: '',
      QuotedPrice: 0,
      FinalPrice: 0,
      IsFieldworkComplete: false,
      IsDrawingComplete: false,
      IsScanned: false,
      IsDelivered: false,
    });
  };

  const handleModalClose = () => {
    setIsCreateModalOpen(false);
    setIsEditModalOpen(false);
    setEditingSurvey(null);
    setPrefilledStatusId(null);
    resetForm();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingSurvey) {
        await updateSurvey(editingSurvey.SurveyId, formData);
      } else {
        await createSurvey(formData);
      }
      refetch(); // Refresh the board data
      handleModalClose();
    } catch (error) {
      console.error('Failed to save survey:', error);
    }
  };

  // Column management handlers
  const handleCreateStatus = async () => {
    if (!newStatusName.trim()) return;
    
    try {
      await createSurveyStatus({
        StatusName: newStatusName.trim(),
        Description: '',
        IsActive: true
      });
      setNewStatusName('');
      refetchStatuses();
    } catch (error) {
      console.error('Failed to create status:', error);
    }
  };

  const handleRenameStatus = async (status: SurveyStatus, newName: string) => {
    if (!newName.trim() || newName === status.StatusName) {
      setEditingStatus(null);
      return;
    }
    
    try {
      // Skip updating the 'unknown' status as it's not a real database record
      if (status.SurveyStatusId === 'unknown') {
        console.log('Cannot rename the Unknown Status column');
        setEditingStatus(null);
        return;
      }
      
      await updateSurveyStatus(status.SurveyStatusId, {
        StatusName: newName.trim()
      });
      
      setEditingStatus(null);
    } catch (error) {
      console.error('Error renaming status:', error);
      setEditingStatus(null);
    }
  };

  // Column drag and drop handlers
  const handleColumnDragStart = (e: React.DragEvent, statusId: string) => {
    setDraggedColumn(statusId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleColumnDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleColumnDrop = (e: React.DragEvent, targetStatusId: string) => {
    e.preventDefault();
    
    if (!draggedColumn || draggedColumn === targetStatusId) {
      setDraggedColumn(null);
      return;
    }

    const newOrder = [...columnOrder];
    const draggedIndex = newOrder.indexOf(draggedColumn);
    const targetIndex = newOrder.indexOf(targetStatusId);
    
    // Remove dragged item and insert at new position
    newOrder.splice(draggedIndex, 1);
    newOrder.splice(targetIndex, 0, draggedColumn);
    
    setColumnOrder(newOrder);
    setDraggedColumn(null);
  };

  // Drag and drop handlers
  const handleDragStart = (survey: Survey) => {
    setDraggedSurvey(survey);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault(); // Allow drop
  };

  const handleDragEnter = (statusId: string) => {
    setDragOverColumn(statusId);
  };

  const handleDragLeave = () => {
    setDragOverColumn(null);
  };

  const handleDrop = async (e: React.DragEvent, targetStatusId: string) => {
    e.preventDefault();
    setDragOverColumn(null);

    if (!draggedSurvey || draggedSurvey.StatusId === targetStatusId) {
      setDraggedSurvey(null);
      return;
    }

    try {
      // Set updating state
      setUpdatingSurveyId(draggedSurvey.SurveyId);
      
      // Update the survey status
      await updateSurvey(draggedSurvey.SurveyId, {
        StatusId: targetStatusId
      });

      // Optimistically update the local state
      setGroupedSurveys(prev => {
        const newGrouped = { ...prev };
        
        // Remove from old status
        const oldStatusId = draggedSurvey.StatusId || 'unknown';
        if (newGrouped[oldStatusId]) {
          newGrouped[oldStatusId] = newGrouped[oldStatusId].filter(
            s => s.SurveyId !== draggedSurvey.SurveyId
          );
        }
        
        // Add to new status
        if (!newGrouped[targetStatusId]) {
          newGrouped[targetStatusId] = [];
        }
        newGrouped[targetStatusId].push({
          ...draggedSurvey,
          StatusId: targetStatusId
        });
        
        return newGrouped;
      });

      // Success - the optimistic update is sufficient
      console.log('Survey status updated successfully');
    } catch (error) {
      console.error('Failed to update survey status:', error);
      
      // On error, refetch to restore correct state
      refetch();
      
      // Optionally show error message to user
    } finally {
      setDraggedSurvey(null);
      setUpdatingSurveyId(null);
    }
  };

  if (surveysLoading || statusesLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="flex space-x-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="w-80 h-96 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (surveysError) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <h3 className="text-red-800 font-medium">Error loading board data</h3>
          <p className="text-red-600 text-sm mt-1">
            Unable to load surveys and statuses. Please try again.
          </p>
          <button 
            onClick={() => refetch()}
            className="mt-3 bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const activeStatuses = statusesData?.filter(status => status.IsActive) || [];
  const hiddenStatuses = activeStatuses.filter(status => hiddenColumns.has(status.SurveyStatusId));
  
  // Order statuses based on columnOrder, then add any missing ones
  const orderedStatuses = columnOrder
    .map(id => activeStatuses.find(status => status.SurveyStatusId === id))
    .filter((status): status is SurveyStatus => status !== undefined)
    .concat(activeStatuses.filter(status => !columnOrder.includes(status.SurveyStatusId)));

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Survey Board</h1>
        <p className="mt-2 text-gray-600">
          Kanban-style view of surveys organized by status
        </p>
      </div>

      {/* Search and filters */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex-1 max-w-md">
              <input
                type="text"
                placeholder="Search surveys..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div className="text-sm text-gray-500">
              Total: {surveysData?.total || 0} surveys
            </div>
          </div>
          
          {/* Column visibility controls */}
          <div className="flex items-center space-x-4">
            {hiddenStatuses.length > 0 && (
              <div className="flex items-center space-x-2">
                <AdjustmentsHorizontalIcon className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-500">Hidden columns:</span>
                {hiddenStatuses.map((status) => (
                  <button
                    key={status.SurveyStatusId}
                    onClick={() => handleShowColumn(status.SurveyStatusId)}
                    className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
                    title={`Show ${status.StatusName} column`}
                  >
                    <EyeIcon className="h-3 w-3 mr-1" />
                    {status.StatusName}
                  </button>
                ))}
                {hiddenStatuses.length > 1 && (
                  <button
                    onClick={handleShowAllColumns}
                    className="text-xs text-indigo-600 hover:text-indigo-800 underline"
                  >
                    Show all
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Board columns */}
      <div className="flex space-x-6 overflow-x-auto pb-6">
        {orderedStatuses
          .filter(status => !hiddenColumns.has(status.SurveyStatusId))
          .map((status) => {
            const surveys = groupedSurveys[status.SurveyStatusId] || [];
            return (
              <div
                key={status.SurveyStatusId}
                draggable
                onDragStart={(e) => handleColumnDragStart(e, status.SurveyStatusId)}
                onDragOver={handleColumnDragOver}
                onDrop={(e) => handleColumnDrop(e, status.SurveyStatusId)}
                className={`${draggedColumn === status.SurveyStatusId ? 'opacity-50' : ''}`}
              >
                <BoardColumn
                  status={status}
                  surveys={surveys}
                  onHide={handleHideColumn}
                  onDragStart={handleDragStart}
                  onDragOver={(e) => {
                    handleDragOver(e);
                    handleDragEnter(status.SurveyStatusId);
                  }}
                  onDrop={handleDrop}
                  isDragOver={dragOverColumn === status.SurveyStatusId}
                  updatingSurveyId={updatingSurveyId}
                  onCreateSurvey={handleCreateSurvey}
                  onEdit={handleEditSurvey}
                  onRenameStatus={(newName) => handleRenameStatus(status, newName)}
                  editingStatus={editingStatus}
                  setEditingStatus={setEditingStatus}
                />
              </div>
            );
          })}
        
        {/* Unknown status column for surveys without a valid status */}
        {groupedSurveys['unknown'] && 
         groupedSurveys['unknown'].length > 0 && 
         !hiddenColumns.has('unknown') && (
          <BoardColumn
            status={{
              SurveyStatusId: 'unknown',
              StatusName: 'Unknown Status',
              Description: 'Surveys with unrecognized status',
              IsActive: true
            }}
            surveys={groupedSurveys['unknown']}
            onHide={handleHideColumn}
            onDragStart={handleDragStart}
            onDragOver={(e) => {
              handleDragOver(e);
              handleDragEnter('unknown');
            }}
            onDrop={handleDrop}
            isDragOver={dragOverColumn === 'unknown'}
            updatingSurveyId={updatingSurveyId}
            onCreateSurvey={handleCreateSurvey}
            onEdit={handleEditSurvey}
            onRenameStatus={(newName) => handleRenameStatus({ SurveyStatusId: 'unknown', StatusName: 'Unknown Status', Description: 'Surveys with unrecognized status', IsActive: true }, newName)}
            editingStatus={editingStatus}
            setEditingStatus={setEditingStatus}
          />
        )}
      </div>

      {/* Create/Edit Survey Modal */}
      {(isCreateModalOpen || isEditModalOpen) && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {editingSurvey ? 'Edit Survey' : 'Create New Survey'}
              </h3>
              <button
                onClick={handleModalClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Survey Number */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Survey Number*</label>
                  <input
                    type="text"
                    required
                    value={formData.SurveyNumber}
                    onChange={(e) => setFormData({ ...formData, SurveyNumber: e.target.value })}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>

                {/* Title */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Title</label>
                  <input
                    type="text"
                    value={formData.Title}
                    onChange={(e) => setFormData({ ...formData, Title: e.target.value })}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>

                {/* Customer */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Customer</label>
                  <select
                    value={formData.CustomerId || ''}
                    onChange={(e) => setFormData({ ...formData, CustomerId: e.target.value || undefined })}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">Select Customer</option>
                    {customersData?.customers?.map((customer) => (
                      <option key={customer.CustomerId} value={customer.CustomerId}>
                        {customer.CompanyName}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Survey Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Survey Type</label>
                  <select
                    value={formData.SurveyTypeId || ''}
                    onChange={(e) => setFormData({ ...formData, SurveyTypeId: e.target.value || undefined })}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">Select Type</option>
                    {surveyTypesData?.map((type) => (
                      <option key={type.SurveyTypeId} value={type.SurveyTypeId}>
                        {type.SurveyTypeName}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Status (pre-filled) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Status</label>
                  <select
                    value={formData.StatusId || ''}
                    onChange={(e) => setFormData({ ...formData, StatusId: e.target.value || undefined })}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 bg-blue-50"
                  >
                    <option value="">Select Status</option>
                    {statusesData?.map((status) => (
                      <option key={status.SurveyStatusId} value={status.SurveyStatusId}>
                        {status.StatusName}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Quoted Price */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Quoted Price</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.QuotedPrice || ''}
                    onChange={(e) => setFormData({ ...formData, QuotedPrice: parseFloat(e.target.value) || 0 })}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  rows={3}
                  value={formData.Description}
                  onChange={(e) => setFormData({ ...formData, Description: e.target.value })}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>

              {/* Form Actions */}
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={handleModalClose}
                  className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createLoading || updateLoading}
                  className="px-4 py-2 bg-indigo-600 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createLoading || updateLoading ? 
                    (editingSurvey ? 'Updating...' : 'Creating...') : 
                    (editingSurvey ? 'Update Survey' : 'Create Survey')
                  }
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}