import React, { useState, useEffect } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { Property, PropertyCreate } from '../types';
import Modal from '../components/Modal';
import SearchBar from '../components/SearchBar';
import Pagination from '../components/Pagination';
import { 
  useProperties, 
  useCreateProperty, 
  useUpdateProperty, 
  useDeleteProperty,
  useTownships
} from '../hooks/useGraphQLApi';

export default function Properties() {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProperty, setEditingProperty] = useState<Property | null>(null);
  const [formData, setFormData] = useState<PropertyCreate>({
    PropertyCode: '',
    PropertyName: '',
    PropertyDescription: '',
    OwnerName: '',
    OwnerPhone: '',
    OwnerEmail: '',
    AddressId: '',
    TownshipId: '',
    IsActive: true,
    // Legacy fields
    SurveyPrimaryKey: 0,
    LegacyTax: '',
    District: '',
    Section: '',
    Block: '',
    Lot: '',
    PropertyType: '',
  });

  const pageSize = 20;

  // GraphQL hooks
  const { data: propertiesData, loading, error, refetch } = useProperties(currentPage, pageSize, searchTerm || undefined);
  const { create: createProperty, loading: createLoading } = useCreateProperty();
  const { update: updateProperty, loading: updateLoading } = useUpdateProperty();
  const { remove: deleteProperty } = useDeleteProperty();
  
  // Lookup data
  const { data: townships } = useTownships(1, 1000); // Get all townships for dropdown

  const properties = propertiesData?.properties || [];
  const totalPages = propertiesData ? Math.ceil(propertiesData.total / pageSize) : 1;

  useEffect(() => {
    refetch();
  }, [currentPage, searchTerm, refetch]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingProperty) {
        await updateProperty(editingProperty.PropertyId, formData);
      } else {
        await createProperty(formData);
      }
      setIsModalOpen(false);
      setEditingProperty(null);
      resetForm();
      refetch();
    } catch (err) {
      console.error('Failed to save property:', err);
    }
  };

  const handleDelete = async (property: Property) => {
    if (window.confirm(`Are you sure you want to delete property ${property.District}-${property.Section}-${property.Block}-${property.Lot}?`)) {
      try {
        await deleteProperty(property.PropertyId);
        refetch();
      } catch (err) {
        console.error('Failed to delete property:', err);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      PropertyCode: '',
      PropertyName: '',
      PropertyDescription: '',
      OwnerName: '',
      OwnerPhone: '',
      OwnerEmail: '',
      AddressId: '',
      TownshipId: '',
      IsActive: true,
      // Legacy fields
      SurveyPrimaryKey: 0,
      LegacyTax: '',
      District: '',
      Section: '',
      Block: '',
      Lot: '',
      PropertyType: '',
    });
  };

  const openModal = (property?: Property) => {
    if (property) {
      setEditingProperty(property);
      setFormData({
        PropertyCode: property.PropertyCode || '',
        PropertyName: property.PropertyName || '',
        PropertyDescription: property.PropertyDescription || '',
        OwnerName: property.OwnerName || '',
        OwnerPhone: property.OwnerPhone || '',
        OwnerEmail: property.OwnerEmail || '',
        AddressId: property.AddressId || '',
        TownshipId: property.TownshipId || '',
        IsActive: property.IsActive,
        // Legacy fields
        SurveyPrimaryKey: property.SurveyPrimaryKey || 0,
        LegacyTax: property.LegacyTax || '',
        District: property.District || '',
        Section: property.Section || '',
        Block: property.Block || '',
        Lot: property.Lot || '',
        PropertyType: property.PropertyType || '',
      });
    } else {
      setEditingProperty(null);
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
          <h1 className="text-2xl font-bold text-gray-900">Properties</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage property records and their details.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            type="button"
            onClick={() => openModal()}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
          >
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Add Property
          </button>
        </div>
      </div>

      <div className="mt-4">
        <SearchBar
          value={searchTerm}
          onChange={setSearchTerm}
          placeholder="Search properties..."
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
                      District
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Section
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Block
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Lot
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Legacy Tax
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Township
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Property Type
                    </th>
                    <th scope="col" className="relative px-6 py-3">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {properties.map((property) => (
                    <tr key={property.PropertyId}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {property.District}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {property.Section}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {property.Block}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {property.Lot}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {property.LegacyTax || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {townships?.townships?.find(t => t.TownshipId === property.TownshipId)?.TownshipName || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {property.PropertyType || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => openModal(property)}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          <PencilIcon className="h-5 w-5" aria-hidden="true" />
                        </button>
                        <button
                          onClick={() => handleDelete(property)}
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

      {/* Modal for creating/editing properties */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingProperty ? 'Edit Property' : 'Create New Property'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="propertyCode" className="block text-sm font-medium text-gray-700">
                Property Code *
              </label>
              <input
                type="text"
                id="propertyCode"
                required
                value={formData.PropertyCode}
                onChange={(e) => setFormData({ ...formData, PropertyCode: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="propertyName" className="block text-sm font-medium text-gray-700">
                Property Name *
              </label>
              <input
                type="text"
                id="propertyName"
                required
                value={formData.PropertyName}
                onChange={(e) => setFormData({ ...formData, PropertyName: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>
          <div>
            <label htmlFor="propertyDescription" className="block text-sm font-medium text-gray-700">
              Property Description
            </label>
            <textarea
              id="propertyDescription"
              value={formData.PropertyDescription}
              onChange={(e) => setFormData({ ...formData, PropertyDescription: e.target.value })}
              rows={3}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="ownerName" className="block text-sm font-medium text-gray-700">
                Owner Name
              </label>
              <input
                type="text"
                id="ownerName"
                value={formData.OwnerName}
                onChange={(e) => setFormData({ ...formData, OwnerName: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="ownerPhone" className="block text-sm font-medium text-gray-700">
                Owner Phone
              </label>
              <input
                type="tel"
                id="ownerPhone"
                value={formData.OwnerPhone}
                onChange={(e) => setFormData({ ...formData, OwnerPhone: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>
          <div>
            <label htmlFor="ownerEmail" className="block text-sm font-medium text-gray-700">
              Owner Email
            </label>
            <input
              type="email"
              id="ownerEmail"
              value={formData.OwnerEmail}
              onChange={(e) => setFormData({ ...formData, OwnerEmail: e.target.value })}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="district" className="block text-sm font-medium text-gray-700">
                District
              </label>
              <input
                type="text"
                id="district"
                value={formData.District}
                onChange={(e) => setFormData({ ...formData, District: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="section" className="block text-sm font-medium text-gray-700">
                Section
              </label>
              <input
                type="text"
                id="section"
                value={formData.Section}
                onChange={(e) => setFormData({ ...formData, Section: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="block" className="block text-sm font-medium text-gray-700">
                Block *
              </label>
              <input
                type="text"
                id="block"
                required
                value={formData.Block}
                onChange={(e) => setFormData({ ...formData, Block: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="lot" className="block text-sm font-medium text-gray-700">
                Lot *
              </label>
              <input
                type="text"
                id="lot"
                required
                value={formData.Lot}
                onChange={(e) => setFormData({ ...formData, Lot: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="legacyTax" className="block text-sm font-medium text-gray-700">
                Legacy Tax
              </label>
              <input
                type="text"
                id="legacyTax"
                value={formData.LegacyTax}
                onChange={(e) => setFormData({ ...formData, LegacyTax: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="surveyPrimaryKey" className="block text-sm font-medium text-gray-700">
                Survey Primary Key
              </label>
              <input
                type="number"
                id="surveyPrimaryKey"
                value={formData.SurveyPrimaryKey}
                onChange={(e) => setFormData({ ...formData, SurveyPrimaryKey: parseInt(e.target.value) || 0 })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="townshipId" className="block text-sm font-medium text-gray-700">
                Township
              </label>
              <select
                id="townshipId"
                value={formData.TownshipId}
                onChange={(e) => setFormData({ ...formData, TownshipId: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="">Select a township...</option>
                {townships?.townships?.map((township) => (
                  <option key={township.TownshipId} value={township.TownshipId}>
                    {township.TownshipName}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="propertyType" className="block text-sm font-medium text-gray-700">
                Property Type
              </label>
              <input
                type="text"
                id="propertyType"
                value={formData.PropertyType}
                onChange={(e) => setFormData({ ...formData, PropertyType: e.target.value })}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="e.g., Residential, Commercial, Industrial"
              />
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
              {createLoading || updateLoading ? 'Saving...' : (editingProperty ? 'Update' : 'Create')}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
