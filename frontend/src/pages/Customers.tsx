import React, { useState, useEffect, useCallback } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { customerApi } from '../api';
import { Customer, CustomerCreate } from '../types';
import Modal from '../components/Modal';
import SearchBar from '../components/SearchBar';
import Pagination from '../components/Pagination';

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);
  const [formData, setFormData] = useState<CustomerCreate>({
    CustomerCode: '',
    CompanyName: '',
    ContactFirstName: '',
    ContactLastName: '',
    Email: '',
    Phone: '',
    Fax: '',
    Website: '',
    IsActive: true,
  });

  const pageSize = 20;

  const fetchCustomers = useCallback(async () => {
    try {
      setLoading(true);
      const response = await customerApi.getAll(currentPage, pageSize, searchTerm || undefined);
      setCustomers(response.customers);
      setTotalPages(Math.ceil(response.total / pageSize));
    } catch (err) {
      setError('Failed to fetch customers');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [currentPage, searchTerm]);

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingCustomer) {
        await customerApi.update(editingCustomer.CustomerId, formData);
      } else {
        await customerApi.create(formData);
      }
      setIsModalOpen(false);
      setEditingCustomer(null);
      resetForm();
      fetchCustomers();
    } catch (err) {
      setError('Failed to save customer');
      console.error(err);
    }
  };

  const handleEdit = (customer: Customer) => {
    setEditingCustomer(customer);
    setFormData({
      CustomerCode: customer.CustomerCode,
      CompanyName: customer.CompanyName,
      ContactFirstName: customer.ContactFirstName || '',
      ContactLastName: customer.ContactLastName || '',
      Email: customer.Email || '',
      Phone: customer.Phone || '',
      Fax: customer.Fax || '',
      Website: customer.Website || '',
      IsActive: customer.IsActive,
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (customer: Customer) => {
    if (window.confirm(`Are you sure you want to delete ${customer.CompanyName}?`)) {
      try {
        await customerApi.delete(customer.CustomerId);
        fetchCustomers();
      } catch (err) {
        setError('Failed to delete customer');
        console.error(err);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      CustomerCode: '',
      CompanyName: '',
      ContactFirstName: '',
      ContactLastName: '',
      Email: '',
      Phone: '',
      Fax: '',
      Website: '',
      IsActive: true,
    });
  };

  const openCreateModal = () => {
    resetForm();
    setEditingCustomer(null);
    setIsModalOpen(true);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Customers</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all customers in your system including their company name, contact information, and status.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            type="button"
            onClick={openCreateModal}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
          >
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Add Customer
          </button>
        </div>
      </div>

      <div className="mt-6">
        <SearchBar
          value={searchTerm}
          onChange={setSearchTerm}
          placeholder="Search customers..."
        />
      </div>

      {error && (
        <div className="mt-4 rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
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
                      Customer Code
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Company
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Contact
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" className="relative px-6 py-3">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {customers.map((customer) => (
                    <tr key={customer.CustomerId}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {customer.CustomerCode}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {customer.CompanyName}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {customer.ContactFirstName && customer.ContactLastName 
                          ? `${customer.ContactFirstName} ${customer.ContactLastName}`
                          : '-'
                        }
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {customer.Email || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          customer.IsActive 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {customer.IsActive ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleEdit(customer)}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          <PencilIcon className="h-5 w-5" />
                        </button>
                        <button
                          onClick={() => handleDelete(customer)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <TrashIcon className="h-5 w-5" />
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

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingCustomer ? 'Edit Customer' : 'Create Customer'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="customerCode" className="block text-sm font-medium text-gray-700">
                Customer Code
              </label>
              <input
                type="text"
                id="customerCode"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.CustomerCode}
                onChange={(e) => setFormData({ ...formData, CustomerCode: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="companyName" className="block text-sm font-medium text-gray-700">
                Company Name
              </label>
              <input
                type="text"
                id="companyName"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.CompanyName}
                onChange={(e) => setFormData({ ...formData, CompanyName: e.target.value })}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="contactFirstName" className="block text-sm font-medium text-gray-700">
                First Name
              </label>
              <input
                type="text"
                id="contactFirstName"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.ContactFirstName}
                onChange={(e) => setFormData({ ...formData, ContactFirstName: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="contactLastName" className="block text-sm font-medium text-gray-700">
                Last Name
              </label>
              <input
                type="text"
                id="contactLastName"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.ContactLastName}
                onChange={(e) => setFormData({ ...formData, ContactLastName: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              id="email"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              value={formData.Email}
              onChange={(e) => setFormData({ ...formData, Email: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Phone
              </label>
              <input
                type="tel"
                id="phone"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.Phone}
                onChange={(e) => setFormData({ ...formData, Phone: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="website" className="block text-sm font-medium text-gray-700">
                Website
              </label>
              <input
                type="url"
                id="website"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.Website}
                onChange={(e) => setFormData({ ...formData, Website: e.target.value })}
              />
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="isActive"
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              checked={formData.IsActive}
              onChange={(e) => setFormData({ ...formData, IsActive: e.target.checked })}
            />
            <label htmlFor="isActive" className="ml-2 block text-sm text-gray-900">
              Active
            </label>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              {editingCustomer ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
