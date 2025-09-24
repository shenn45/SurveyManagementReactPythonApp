import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { EyeIcon, EyeSlashIcon, AdjustmentsHorizontalIcon, XMarkIcon, PencilIcon } from '@heroicons/react/24/outline';
import { useSurveys, useSurveyStatuses, useUpdateSurvey, useCreateSurvey, useCustomers, useSurveyTypes, useUpdateSurveyStatus, useDefaultBoardConfiguration, useUpdateBoardConfiguration, useBoardConfigurationBySlug } from '../hooks/useGraphQLApi';
import { useBoardSettings } from '../hooks/useBoardSettings';
import { Survey, SurveyStatus, SurveyCreate } from '../types';

interface SurveyCardProps {
  survey: Survey;
  onDragStart: (survey: Survey) => void;
  isUpdating?: boolean;
  onEdit: (survey: Survey) => void;
}

const SurveyCard: React.FC<SurveyCardProps> = ({ survey, onDragStart, isUpdating = false, onEdit }) => {
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

interface BoardColumnProps {
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

const BoardColumn: React.FC<BoardColumnProps> = ({ 
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
  const { boardSlug } = useParams<{ boardSlug: string }>();
  const navigate = useNavigate();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [draggedSurvey, setDraggedSurvey] = useState<Survey | null>(null);
  const [dragOverColumn, setDragOverColumn] = useState<string | null>(null);
  const [updatingSurveyId, setUpdatingSurveyId] = useState<string | null>(null);
  
  // Board configuration state
  const [isEditingBoardName, setIsEditingBoardName] = useState(false);
  const [boardName, setBoardName] = useState(''); // Start with empty string to avoid showing wrong name initially
  const [tempBoardName, setTempBoardName] = useState('');
  
  // Modal state
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingSurvey, setEditingSurvey] = useState<Survey | null>(null);
  const [prefilledStatusId, setPrefilledStatusId] = useState<string | null>(null);
  
  // Board settings hook (replaces localStorage)
  const {
    settings: boardSettings,
    isLoading: settingsLoading,
    error: settingsError,
    hideColumn,
    showColumn,
    showAllColumns,
    updateColumnOrder
  } = useBoardSettings();
  
  // Column management state
  const [editingStatus, setEditingStatus] = useState<SurveyStatus | null>(null);
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
  
  // Fetch all surveys once on initial load (no search parameter - load everything)
  const { data: surveysData, loading: surveysLoading, error: surveysError, refetch } = useSurveys(1, 1000);
  const { data: statusesData, loading: statusesLoading } = useSurveyStatuses();
  const { update: updateSurvey, loading: updateLoading } = useUpdateSurvey();
  const { create: createSurvey, loading: createLoading } = useCreateSurvey();
  const { data: customersData } = useCustomers(1, 1000);
  const { data: surveyTypesData } = useSurveyTypes();
  const { update: updateSurveyStatus } = useUpdateSurveyStatus();

  // Board configuration hooks - use slug if provided, otherwise default
  const { data: boardConfigurationBySlug, loading: boardConfigBySlugLoading, refetch: refetchBoardConfigBySlug } = useBoardConfigurationBySlug(boardSlug || '');
  const { data: defaultBoardConfiguration, loading: defaultBoardConfigLoading, refetch: refetchDefaultBoardConfig } = useDefaultBoardConfiguration();
  const { update: updateBoardConfiguration } = useUpdateBoardConfiguration();

  // Determine which board configuration to use
  const boardConfiguration = boardSlug ? boardConfigurationBySlug : defaultBoardConfiguration;
  const boardConfigLoading = boardSlug ? boardConfigBySlugLoading : defaultBoardConfigLoading;
  const refetchBoardConfig = boardSlug ? refetchBoardConfigBySlug : refetchDefaultBoardConfig;

  const [groupedSurveys, setGroupedSurveys] = useState<{ [key: string]: Survey[] }>({});

  // Memoize the search handler to prevent recreating on every render
  const handleSearchChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('Search input changed:', e.target.value);
    e.preventDefault(); // Prevent any default form behavior
    setSearchTerm(e.target.value);
  }, []);

  // Memoize client-side filtered surveys for instant search results
  const filteredSurveys = useMemo(() => {
    if (!surveysData?.surveys) return [];
    
    if (!searchTerm.trim()) {
      return surveysData.surveys;
    }
    
    const searchLower = searchTerm.toLowerCase();
    return surveysData.surveys.filter(survey => 
      survey.SurveyNumber?.toLowerCase().includes(searchLower) ||
      survey.Title?.toLowerCase().includes(searchLower) ||
      survey.Description?.toLowerCase().includes(searchLower) ||
      survey.PurposeCode?.toLowerCase().includes(searchLower) ||
      // Search by customer name if available
      (customersData?.customers?.find(c => c.CustomerId === survey.CustomerId)?.CompanyName?.toLowerCase().includes(searchLower)) ||
      // Search by survey type if available  
      (surveyTypesData?.find(st => st.SurveyTypeId === survey.SurveyTypeId)?.SurveyTypeName?.toLowerCase().includes(searchLower))
    );
  }, [surveysData?.surveys, searchTerm, customersData?.customers, surveyTypesData]);


  // Initialize column order when statuses are loaded or settings change
  useEffect(() => {
    if (statusesData && statusesData.length > 0) {
      // If we have saved column order, validate and use it
      if (boardSettings.columnOrder.length > 0) {
        const validOrder = boardSettings.columnOrder.filter((id: string) => 
          statusesData.some(status => status.SurveyStatusId === id)
        );
        // Add any new statuses that aren't in the saved order
        const newStatuses = statusesData
          .filter(status => !validOrder.includes(status.SurveyStatusId))
          .map(status => status.SurveyStatusId);
        
        const finalOrder = [...validOrder, ...newStatuses];
        // Only update if the order has actually changed (deep comparison)
        if (JSON.stringify(finalOrder.sort()) !== JSON.stringify(boardSettings.columnOrder.sort())) {
          updateColumnOrder(finalOrder);
        }
      } else {
        // First time - use default order
        const defaultOrder = statusesData.map(status => status.SurveyStatusId);
        // Only update if different from current
        if (JSON.stringify(defaultOrder.sort()) !== JSON.stringify(boardSettings.columnOrder.sort())) {
          updateColumnOrder(defaultOrder);
        }
      }
    }
  }, [statusesData]); // Remove boardSettings.columnOrder and updateColumnOrder from dependencies

  // Sync board configuration with local state
  useEffect(() => {
    if (boardConfiguration?.BoardName && boardConfiguration.BoardName !== boardName) {
      setBoardName(boardConfiguration.BoardName);
    } else if (!boardConfigLoading && !boardConfiguration && boardName !== 'Survey Board') {
      // Only set if different to prevent unnecessary updates
      setBoardName('Survey Board');
    }
  }, [boardConfiguration, boardConfigLoading]); // Remove boardName from dependencies

  // Memoize the surveys grouping to prevent constant recalculation
  const memoizedGroupedSurveys = useMemo(() => {
    if (!filteredSurveys || !statusesData || updatingSurveyId) {
      return groupedSurveys; // Return existing state if updating
    }

    return filteredSurveys.reduce((acc, survey) => {
      const statusId = survey.StatusId || 'unknown';
      if (!acc[statusId]) {
        acc[statusId] = [];
      }
      acc[statusId].push(survey);
      return acc;
    }, {} as { [key: string]: Survey[] });
  }, [filteredSurveys, statusesData, updatingSurveyId, groupedSurveys]);

  // Update the groupedSurveys effect to use memoized value
  useEffect(() => {
    if (JSON.stringify(memoizedGroupedSurveys) !== JSON.stringify(groupedSurveys)) {
      setGroupedSurveys(memoizedGroupedSurveys);
    }
  }, [memoizedGroupedSurveys]); // Remove groupedSurveys from dependency

  const handleHideColumn = (statusId: string) => {
    hideColumn(statusId);
  };

  const handleShowColumn = (statusId: string) => {
    showColumn(statusId);
  };

  const handleShowAllColumns = () => {
    showAllColumns();
  };

  // Memoize create survey handler
  const handleCreateSurvey = useCallback((statusId: string) => {
    setPrefilledStatusId(statusId);
    setFormData(prev => ({ ...prev, StatusId: statusId }));
    setIsCreateModalOpen(true);
  }, []);

  // Memoize edit survey handler
  const handleEditSurvey = useCallback((survey: Survey) => {
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
  }, []);

  // Memoize modal handlers
  const resetForm = useCallback(() => {
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
  }, [prefilledStatusId]);

  const handleModalClose = useCallback(() => {
    setIsCreateModalOpen(false);
    setIsEditModalOpen(false);
    setEditingSurvey(null);
    setPrefilledStatusId(null);
    resetForm();
  }, [resetForm]);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
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
  }, [editingSurvey, updateSurvey, formData, createSurvey, refetch, handleModalClose]);

  // Memoize column management handlers
  const handleRenameStatus = useCallback(async (status: SurveyStatus, newName: string) => {
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
  }, [updateSurveyStatus]);

  // Memoize column drag and drop handlers
  const handleColumnDragStart = useCallback((e: React.DragEvent, statusId: string) => {
    setDraggedColumn(statusId);
    e.dataTransfer.effectAllowed = 'move';
  }, []);

  const handleColumnDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }, []);

  const handleColumnDrop = useCallback((e: React.DragEvent, targetStatusId: string) => {
    e.preventDefault();
    
    if (!draggedColumn || draggedColumn === targetStatusId) {
      setDraggedColumn(null);
      return;
    }

    const newOrder = [...boardSettings.columnOrder];
    const draggedIndex = newOrder.indexOf(draggedColumn);
    const targetIndex = newOrder.indexOf(targetStatusId);
    
    // Remove dragged item and insert at new position
    newOrder.splice(draggedIndex, 1);
    newOrder.splice(targetIndex, 0, draggedColumn);
    
    updateColumnOrder(newOrder);
    setDraggedColumn(null);
  }, [draggedColumn, boardSettings.columnOrder, updateColumnOrder]);

  // Memoize drag and drop handlers
  const handleDragStart = useCallback((survey: Survey) => {
    setDraggedSurvey(survey);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault(); // Allow drop
  }, []);

  const handleDragEnter = useCallback((statusId: string) => {
    setDragOverColumn(statusId);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent, targetStatusId: string) => {
    e.preventDefault();
    setDragOverColumn(null);

    if (!draggedSurvey || draggedSurvey.StatusId === targetStatusId) {
      setDraggedSurvey(null);
      return;
    }

    try {
      // Set updating state
      setUpdatingSurveyId(draggedSurvey.SurveyId);
      
      // Optimistically update the local state first
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

      // Update the survey status
      await updateSurvey(draggedSurvey.SurveyId, {
        StatusId: targetStatusId
      });

      // Success - refresh data to ensure consistency
      await refetch();
      
    } catch (error) {
      console.error('Failed to update survey status:', error);
      
      // On error, refetch to restore correct state
      await refetch();
      
      // Optionally show error message to user
    } finally {
      setDraggedSurvey(null);
      // Clear updating state after a small delay to allow refetch to complete
      setTimeout(() => {
        setUpdatingSurveyId(null);
      }, 100);
    }
  }, [draggedSurvey, updateSurvey, refetch]);

  // Memoize board name functions
  const handleEditBoardName = useCallback(() => {
    setTempBoardName(boardName);
    setIsEditingBoardName(true);
  }, [boardName]);

  const handleSaveBoardName = useCallback(async () => {
    if (tempBoardName.trim() && tempBoardName.trim() !== boardName) {
      try {
        if (boardConfiguration) {
          const newSlug = tempBoardName.trim().toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
          await updateBoardConfiguration(boardConfiguration.BoardConfigId, {
            BoardName: tempBoardName.trim(),
            BoardSlug: newSlug
          });
          
          // Update local state immediately
          setBoardName(tempBoardName.trim());
          
          // Refetch to ensure cache is updated
          await refetchBoardConfig();
          
          // Navigate to new slug route if it changed
          if (!boardSlug || boardSlug !== newSlug) {
            navigate(`/board/${newSlug}`, { replace: true });
          }
        }
      } catch (error) {
        console.error('Failed to update board name:', error);
        // Optionally show error message to user
      }
    }
    setIsEditingBoardName(false);
    setTempBoardName('');
  }, [tempBoardName, boardName, boardConfiguration, updateBoardConfiguration, refetchBoardConfig, boardSlug, navigate]);

  const handleCancelEditBoardName = useCallback(() => {
    setIsEditingBoardName(false);
    setTempBoardName('');
  }, []);

  const handleBoardNameKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSaveBoardName();
    } else if (e.key === 'Escape') {
      handleCancelEditBoardName();
    }
  }, [handleSaveBoardName, handleCancelEditBoardName]);

  // Memoize computed values to prevent unnecessary recalculations (MUST be before early returns!)
  const activeStatuses = useMemo(() => 
    statusesData?.filter(status => status.IsActive) || [], 
    [statusesData]
  );

  const hiddenStatuses = useMemo(() => 
    activeStatuses.filter(status => boardSettings.hiddenColumns.includes(status.SurveyStatusId)), 
    [activeStatuses, boardSettings.hiddenColumns]
  );
  
  // Memoize ordered statuses based on boardSettings.columnOrder
  const orderedStatuses = useMemo(() => 
    boardSettings.columnOrder
      .map(id => activeStatuses.find(status => status.SurveyStatusId === id))
      .filter((status): status is SurveyStatus => status !== undefined)
      .concat(activeStatuses.filter(status => !boardSettings.columnOrder.includes(status.SurveyStatusId))), 
    [boardSettings.columnOrder, activeStatuses]
  );

  if (surveysLoading || statusesLoading || settingsLoading) {
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

  // Show settings error as warning (non-blocking)
  const settingsWarning = settingsError && (
    <div className="mb-4 bg-yellow-50 border border-yellow-200 rounded-md p-3">
      <p className="text-yellow-800 text-sm">
        ⚠️ Unable to load board preferences from database. Using local settings as fallback.
      </p>
    </div>
  );

  return (
    <div className="p-8">
      <div className="mb-8">
        <div className="flex items-center space-x-2">
          {isEditingBoardName ? (
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={tempBoardName}
                onChange={(e) => setTempBoardName(e.target.value)}
                onKeyDown={handleBoardNameKeyDown}
                onBlur={handleSaveBoardName}
                className="text-2xl font-bold text-gray-900 bg-transparent border-2 border-blue-500 rounded px-2 py-1 focus:outline-none focus:border-blue-700"
                autoFocus
              />
              <button
                onClick={handleSaveBoardName}
                className="p-1 text-green-600 hover:text-green-800"
                title="Save"
              >
                ✓
              </button>
              <button
                onClick={handleCancelEditBoardName}
                className="p-1 text-red-600 hover:text-red-800"
                title="Cancel"
              >
                ✕
              </button>
            </div>
          ) : (
            <div className="flex items-center space-x-2 group">
              {boardConfigLoading ? (
                <div className="h-8 w-48 bg-gray-200 rounded animate-pulse"></div>
              ) : (
                <>
                  <h1 className="text-2xl font-bold text-gray-900">
                    {boardName || 'Survey Board'}
                  </h1>
                  <button
                    onClick={handleEditBoardName}
                    className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-gray-600 transition-opacity"
                    title="Edit board name"
                  >
                    <PencilIcon className="w-4 h-4" />
                  </button>
                </>
              )}
            </div>
          )}
        </div>
        <p className="mt-2 text-gray-600">
          Kanban-style view of surveys organized by status
        </p>
      </div>

      {/* Settings error warning */}
      {settingsWarning}

      {/* Search and filters */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex-1 max-w-md">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search surveys by number, title, description, customer, or type..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
                {searchTerm && (
                  <button
                    onClick={() => setSearchTerm('')}
                    className="absolute right-2 top-2 text-gray-400 hover:text-gray-600"
                    title="Clear search"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>
            <div className="text-sm text-gray-500">
              {searchTerm ? (
                <>
                  Showing {filteredSurveys.length} of {surveysData?.total || 0} surveys
                  {filteredSurveys.length !== (surveysData?.total || 0) && (
                    <span className="ml-2 text-blue-600 font-medium">
                      (filtered)
                    </span>
                  )}
                </>
              ) : (
                <>Total: {surveysData?.total || 0} surveys</>
              )}
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
          .filter(status => !boardSettings.hiddenColumns.includes(status.SurveyStatusId))
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
         !boardSettings.hiddenColumns.includes('unknown') && (
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