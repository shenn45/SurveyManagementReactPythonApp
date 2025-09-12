import React, { useState, useEffect } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { Survey, SurveyCreate } from '../types';
import Modal from '../components/Modal';
import SearchBar from '../components/SearchBar';
import Pagination from '../components/Pagination';
import { 
  useSurveys, 
  useCreateSurvey, 
  useUpdateSurvey, 
  useDeleteSurvey,
  useCustomers,
  useProperties,
  useSurveyTypes,
  useSurveyStatuses
} from '../hooks/useGraphQLApi';

export default function Surveys() {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSurvey, setEditingSurvey] = useState<Survey | null>(null);
  const [formData, setFormData] = useState<SurveyCreate>({
    SurveyNumber: '',
    CustomerId: 0,
    PropertyId: 0,
    SurveyTypeId: 0,
    StatusId: 0,
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

  const pageSize = 20;

  // GraphQL hooks
  const { data: surveysData, loading, error, refetch } = useSurveys(currentPage, pageSize, searchTerm || undefined);
  const { create: createSurvey, loading: createLoading } = useCreateSurvey();
  const { update: updateSurvey, loading: updateLoading } = useUpdateSurvey();
  const { remove: deleteSurvey } = useDeleteSurvey();
  
  // Lookup data
  const { data: customersData } = useCustomers(1, 1000); // Get all customers for dropdown
  const { data: propertiesData } = useProperties(1, 1000); // Get all properties for dropdown
  const { data: surveyTypes } = useSurveyTypes();
  const { data: surveyStatuses } = useSurveyStatuses();

  const surveys = surveysData?.surveys || [];
  const totalPages = surveysData ? Math.ceil(surveysData.total / pageSize) : 1;

  useEffect(() => {
    refetch();
  }, [currentPage, searchTerm, refetch]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingSurvey) {
        await updateSurvey(editingSurvey.SurveyId, formData);
      } else {
        await createSurvey(formData);
      }
      setIsModalOpen(false);
      setEditingSurvey(null);
      resetForm();
      refetch();
    } catch (err) {
      console.error('Failed to save survey:', err);
    }
  };

  const handleDelete = async (survey: Survey) => {
    if (window.confirm(`Are you sure you want to delete survey ${survey.SurveyNumber}?`)) {
      try {
        await deleteSurvey(survey.SurveyId);
        refetch();
      } catch (err) {
        console.error('Failed to delete survey:', err);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      SurveyNumber: '',
      CustomerId: 0,
      PropertyId: 0,
      SurveyTypeId: 0,
      StatusId: 0,
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

  const openModal = (survey?: Survey) => {
    if (survey) {
      setEditingSurvey(survey);
      setFormData({
        SurveyNumber: survey.SurveyNumber,
        CustomerId: survey.CustomerId,
        PropertyId: survey.PropertyId,
        SurveyTypeId: survey.SurveyTypeId,
        StatusId: survey.StatusId,
        Title: survey.Title,
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
    } else {
      setEditingSurvey(null);
      resetForm();
    }
    setIsModalOpen(true);
  };

  if (loading) {
    return (
      <div className="p-8">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-bold text-gray-900">Surveys</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage survey projects and track their progress.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            type="button"
            onClick={() => openModal()}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
          >
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Add Survey
          </button>
        </div>
      </div>

      <div className="mt-4">
        <SearchBar
          value={searchTerm}
          onChange={setSearchTerm}
          placeholder="Search surveys..."
        />
      </div>

      {error && (
        <div className="mt-4 rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error.message || 'An error occurred'}</div>
        </div>
      )}

      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Survey Number
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Title
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Customer
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Request Date
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Due Date
                    </th>
                    <th scope="col" className="relative px-6 py-3">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {surveys.map((survey) => (
                    <tr key={survey.SurveyId}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {survey.SurveyNumber}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {survey.Title}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {customersData?.customers.find(c => c.CustomerId === survey.CustomerId)?.CompanyName || 'Unknown'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {surveyStatuses?.find(s => s.StatusId === survey.StatusId)?.StatusName || 'Unknown'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {survey.RequestDate ? new Date(survey.RequestDate).toLocaleDateString() : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {survey.DueDate ? new Date(survey.DueDate).toLocaleDateString() : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => openModal(survey)}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          <PencilIcon className="h-5 w-5" aria-hidden="true" />
                        </button>
                        <button
                          onClick={() => handleDelete(survey)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <TrashIcon className="h-5 w-5" aria-hidden="true" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
      />

      {/* Modal for creating/editing surveys */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingSurvey ? 'Edit Survey' : 'Create New Survey'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="surveyNumber" className="block text-sm font-medium text-gray-700">
                Survey Number *
              </label>
              <input
                type="text"
                id="surveyNumber"
                required
                value={formData.SurveyNumber}
                onChange={(e) => setFormData({ ...formData, SurveyNumber: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Title *
              </label>
              <input
                type="text"
                id="title"
                required
                value={formData.Title}
                onChange={(e) => setFormData({ ...formData, Title: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="customerId" className="block text-sm font-medium text-gray-700">
                Customer *
              </label>
              <select
                id="customerId"
                required
                value={formData.CustomerId}
                onChange={(e) => setFormData({ ...formData, CustomerId: parseInt(e.target.value) })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value={0}>Select a customer...</option>
                {customersData?.customers.map((customer) => (
                  <option key={customer.CustomerId} value={customer.CustomerId}>
                    {customer.CompanyName}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="propertyId" className="block text-sm font-medium text-gray-700">
                Property
              </label>
              <select
                id="propertyId"
                value={formData.PropertyId}
                onChange={(e) => setFormData({ ...formData, PropertyId: parseInt(e.target.value) })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value={0}>Select a property...</option>
                {propertiesData?.properties.map((property) => (
                  <option key={property.PropertyId} value={property.PropertyId}>
                    {property.District} - {property.Section} - {property.Block} - {property.Lot}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="surveyTypeId" className="block text-sm font-medium text-gray-700">
                Survey Type *
              </label>
              <select
                id="surveyTypeId"
                required
                value={formData.SurveyTypeId}
                onChange={(e) => setFormData({ ...formData, SurveyTypeId: parseInt(e.target.value) })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value={0}>Select a survey type...</option>
                {surveyTypes?.map((type) => (
                  <option key={type.SurveyTypeId} value={type.SurveyTypeId}>
                    {type.TypeName}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="statusId" className="block text-sm font-medium text-gray-700">
                Status *
              </label>
              <select
                id="statusId"
                required
                value={formData.StatusId}
                onChange={(e) => setFormData({ ...formData, StatusId: parseInt(e.target.value) })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value={0}>Select a status...</option>
                {surveyStatuses?.map((status) => (
                  <option key={status.StatusId} value={status.StatusId}>
                    {status.StatusName}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              id="description"
              rows={3}
              value={formData.Description}
              onChange={(e) => setFormData({ ...formData, Description: e.target.value })}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label htmlFor="requestDate" className="block text-sm font-medium text-gray-700">
                Request Date
              </label>
              <input
                type="date"
                id="requestDate"
                value={formData.RequestDate}
                onChange={(e) => setFormData({ ...formData, RequestDate: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="scheduledDate" className="block text-sm font-medium text-gray-700">
                Scheduled Date
              </label>
              <input
                type="date"
                id="scheduledDate"
                value={formData.ScheduledDate}
                onChange={(e) => setFormData({ ...formData, ScheduledDate: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700">
                Due Date
              </label>
              <input
                type="date"
                id="dueDate"
                value={formData.DueDate}
                onChange={(e) => setFormData({ ...formData, DueDate: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="quotedPrice" className="block text-sm font-medium text-gray-700">
                Quoted Price
              </label>
              <input
                type="number"
                id="quotedPrice"
                step="0.01"
                value={formData.QuotedPrice}
                onChange={(e) => setFormData({ ...formData, QuotedPrice: parseFloat(e.target.value) || 0 })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="finalPrice" className="block text-sm font-medium text-gray-700">
                Final Price
              </label>
              <input
                type="number"
                id="finalPrice"
                step="0.01"
                value={formData.FinalPrice}
                onChange={(e) => setFormData({ ...formData, FinalPrice: parseFloat(e.target.value) || 0 })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div className="flex items-center">
              <input
                id="isFieldworkComplete"
                type="checkbox"
                checked={formData.IsFieldworkComplete}
                onChange={(e) => setFormData({ ...formData, IsFieldworkComplete: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="isFieldworkComplete" className="ml-2 block text-sm text-gray-900">
                Fieldwork Complete
              </label>
            </div>
            <div className="flex items-center">
              <input
                id="isDrawingComplete"
                type="checkbox"
                checked={formData.IsDrawingComplete}
                onChange={(e) => setFormData({ ...formData, IsDrawingComplete: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="isDrawingComplete" className="ml-2 block text-sm text-gray-900">
                Drawing Complete
              </label>
            </div>
            <div className="flex items-center">
              <input
                id="isScanned"
                type="checkbox"
                checked={formData.IsScanned}
                onChange={(e) => setFormData({ ...formData, IsScanned: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="isScanned" className="ml-2 block text-sm text-gray-900">
                Scanned
              </label>
            </div>
            <div className="flex items-center">
              <input
                id="isDelivered"
                type="checkbox"
                checked={formData.IsDelivered}
                onChange={(e) => setFormData({ ...formData, IsDelivered: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="isDelivered" className="ml-2 block text-sm text-gray-900">
                Delivered
              </label>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={createLoading || updateLoading}
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {createLoading || updateLoading ? 'Saving...' : (editingSurvey ? 'Update' : 'Create')}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
