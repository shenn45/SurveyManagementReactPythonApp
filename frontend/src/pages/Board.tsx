import React, { useState, useEffect } from 'react';
import { EyeIcon, EyeSlashIcon, AdjustmentsHorizontalIcon } from '@heroicons/react/24/outline';
import { useSurveys, useSurveyStatuses, useUpdateSurvey } from '../hooks/useGraphQLApi';
import { Survey, SurveyStatus } from '../types';

interface SurveyCard {
  survey: Survey;
  onDragStart: (survey: Survey) => void;
}

const SurveyCard: React.FC<SurveyCard> = ({ survey, onDragStart }) => {
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
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-3 hover:shadow-md transition-shadow cursor-move"
      draggable
      onDragStart={() => onDragStart(survey)}
    >
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-medium text-gray-900 truncate">{survey.Title || survey.SurveyNumber}</h4>
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
}

const BoardColumn: React.FC<BoardColumn> = ({ 
  status, 
  surveys, 
  onHide, 
  onDragStart, 
  onDragOver, 
  onDrop,
  isDragOver 
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
          <h3 className={`font-semibold text-sm px-3 py-1 rounded-full ${getHeaderColor(status.StatusName)}`}>
            {status.StatusName}
          </h3>
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
      
      <div className="p-4 max-h-screen overflow-y-auto">
        {surveys.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            <p className="text-sm">No surveys in this status</p>
            <p className="text-xs mt-1">Drop surveys here to update status</p>
          </div>
        ) : (
          surveys.map((survey) => (
            <SurveyCard 
              key={survey.SurveyId} 
              survey={survey} 
              onDragStart={onDragStart}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default function Board() {
  const [searchTerm, setSearchTerm] = useState('');
  const [hiddenColumns, setHiddenColumns] = useState<Set<string>>(new Set());
  const [draggedSurvey, setDraggedSurvey] = useState<Survey | null>(null);
  const [dragOverColumn, setDragOverColumn] = useState<string | null>(null);
  
  // Fetch all surveys (we'll handle filtering on frontend for board view)
  const { data: surveysData, loading: surveysLoading, error: surveysError, refetch } = useSurveys(1, 1000, searchTerm || undefined);
  const { data: statusesData, loading: statusesLoading } = useSurveyStatuses();
  const { update: updateSurvey, loading: updateLoading } = useUpdateSurvey();

  const [groupedSurveys, setGroupedSurveys] = useState<{ [key: string]: Survey[] }>({});

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

      // Refresh data to ensure consistency
      refetch();
    } catch (error) {
      console.error('Failed to update survey status:', error);
      // Optionally show error message to user
    } finally {
      setDraggedSurvey(null);
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
        {activeStatuses
          .filter(status => !hiddenColumns.has(status.SurveyStatusId))
          .map((status) => {
            const surveys = groupedSurveys[status.SurveyStatusId] || [];
            return (
              <BoardColumn
                key={status.SurveyStatusId}
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
              />
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
          />
        )}
      </div>
    </div>
  );
}