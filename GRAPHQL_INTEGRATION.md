# GraphQL Frontend Integration Test

This document describes how to test the GraphQL integration in the Survey Management React App.

## Services Running

1. **Backend GraphQL Server**: http://localhost:8000
   - GraphQL Playground: http://localhost:8000/graphql
   - REST API (still available): http://localhost:8000/api

2. **Frontend React App**: http://localhost:3000
   - Now using GraphQL via Apollo Client

## What Was Updated

### 1. Main App Component (`src/App.tsx`)
- Wrapped application with `ApolloProvider`
- Updated Dashboard to use GraphQL hooks to display real statistics
- Integrated with new Surveys and Properties pages

### 2. Customer Management (`src/pages/Customers.tsx`)
- Replaced REST API calls with GraphQL hooks
- Uses `useCustomers`, `useCreateCustomer`, `useUpdateCustomer`, `useDeleteCustomer`
- Maintained all existing functionality with better performance

### 3. New Survey Management (`src/pages/Surveys.tsx`)
- Full CRUD operations using GraphQL
- Integrated with customer and property lookups
- Survey type and status management
- Progress tracking (fieldwork, drawing, scanning, delivery)

### 4. New Property Management (`src/pages/Properties.tsx`)
- Complete property management interface
- District, Section, Block, Lot organization
- Township integration
- Property type categorization

### 5. GraphQL Infrastructure
- Apollo Client configured (`src/apollo/client.ts`)
- Comprehensive queries and mutations (`src/graphql/queries.ts`)
- Custom React hooks for all operations (`src/hooks/useGraphQLApi.ts`)

## Testing the Integration

### Test GraphQL Queries
1. Open http://localhost:8000/graphql
2. Test a simple query:
```graphql
query GetCustomers {
  customers(limit: 5) {
    customers {
      CustomerId
      CompanyName
      Email
      IsActive
    }
    total
  }
}
```

### Test Frontend Features
1. **Dashboard**: Should show actual counts for Surveys, Customers, and Properties
2. **Customers Page**: Full CRUD operations with GraphQL
3. **Surveys Page**: Create/edit surveys with proper lookups
4. **Properties Page**: Property management with township selection

## Benefits of GraphQL Integration

1. **Efficient Data Fetching**: Only request needed fields
2. **Real-time Updates**: Automatic cache updates after mutations
3. **Type Safety**: Strong typing with TypeScript
4. **Single Endpoint**: All data operations through `/graphql`
5. **Introspection**: Self-documenting API with GraphQL Playground
6. **Optimistic Updates**: Better user experience with instant UI updates

## Environment Variables

Ensure these are set for proper GraphQL endpoint configuration:
- `REACT_APP_GRAPHQL_URL`: http://localhost:8000/graphql (default)

## Architecture

```
Frontend (React + Apollo Client)
    ↕️ GraphQL over HTTP
Backend (FastAPI + Strawberry GraphQL)
    ↕️ SQLAlchemy ORM
Database (SQLite)
```

The frontend now communicates exclusively with the backend via GraphQL, providing a more efficient and modern API integration.
