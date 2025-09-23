import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ApolloProvider } from '@apollo/client/react';
import client from './apollo/client';
import Sidebar from './components/Sidebar';
import Customers from './pages/Customers';
import Surveys from './pages/Surveys';
import Properties from './pages/Properties';
import Townships from './pages/Townships';
import Board from './pages/Board';
import { useCustomers, useSurveys, useProperties } from './hooks/useGraphQLApi';

function Dashboard() {
  const { data: customersData, loading: customersLoading } = useCustomers(1, 1); // Just get count
  const { data: surveysData, loading: surveysLoading } = useSurveys(1, 1); // Just get count
  const { data: propertiesData, loading: propertiesLoading } = useProperties(1, 1); // Just get count

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      <p className="mt-2 text-gray-600">Welcome to the Survey Management System</p>
      
      <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 bg-indigo-500 rounded-md flex items-center justify-center">
                  <span className="text-white font-semibold">S</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Surveys</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {surveysLoading ? 'Loading...' : surveysData?.total || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 bg-green-500 rounded-md flex items-center justify-center">
                  <span className="text-white font-semibold">C</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Active Customers</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {customersLoading ? 'Loading...' : customersData?.total || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <span className="text-white font-semibold">P</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Properties</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {propertiesLoading ? 'Loading...' : propertiesData?.total || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <ApolloProvider client={client}>
      <Router>
        <div className="min-h-screen bg-gray-100 flex">
          <Sidebar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/surveys" element={<Surveys />} />
              <Route path="/board" element={<Board />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/properties" element={<Properties />} />
              <Route path="/townships" element={<Townships />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ApolloProvider>
  );
}

export default App;
