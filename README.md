# Survey Management React App

A full-stack CRUD application for managing surveys, customers, and properties with a Python FastAPI backend and React frontend.

## Quick Start (Automated Setup)

### 🚀 Python 3.13.7 Setup (Recommended for Windows)
```powershell
# Run the Python 3.13.7 setup script
.\setup_python313.ps1
```

This script will:
- Check for Python 3.13.7 installation
- Create a virtual environment
- Install all dependencies
- Set up the project structure

### After Setup
0. **Activate Venv from root if not already activated from previous setup**
   .\venv\Scripts\Activate.ps1

1. **Run Local Dynamo DB** 
   python -m moto.server -p 8001 -H 0.0.0.0

2. **Create DynamoDB tables**:
   python backend\setup_tables.py
   python backend\seed_database.py

3. **Start the backend from the venv** (in a new terminal)::
   python backend\main.py

4. **Start the frontend** (in a new terminal):
   cd frontend
   npm install
   npm start

## Project Structure

```
SurveyManagementReactApp/
├── backend/           # FastAPI Python backend
├── frontend/          # React TypeScript frontend
└── Database Scripts/  # SQL Server database schema
```

## Features

- **Customer Management**: Create, read, update, and delete customer records
- **Survey Management**: Manage survey lifecycle with status tracking
- **Property Management**: Track properties and their details
- **Search & Pagination**: Efficient data browsing with search functionality
- **Responsive UI**: Modern interface built with TailwindCSS and HeadlessUI

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and settings management
- **Boto3**: AWS SDK for DynamoDB operations
- **DynamoDB**: NoSQL database service
- **GraphQL**: Query language with Graphene

### Frontend
- **React 18**: UI library
- **TypeScript**: Type safety
- **TailwindCSS**: Utility-first CSS framework
- **HeadlessUI**: Unstyled, accessible UI components
- **Heroicons**: Beautiful SVG icons
- **React Router**: Client-side routing
- **Axios**: HTTP client

## Getting Started

### Prerequisites
- **Python 3.13.7+** (latest version for optimal performance)
- Node.js 16+
- AWS Account or DynamoDB Local (for NoSQL database)
- Git (for version control)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file based on `.env.example` and configure your database connection.

6. Run the FastAPI development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The React app will be available at `http://localhost:3000`

### Database Setup

1. Execute the SQL script in `Database Scripts/schema.sql` in your SQL Server instance
2. Update the connection string in the backend `.env` file

## API Endpoints

### Customers
- `GET /api/customers` - List customers with pagination and search
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Surveys
- `GET /api/surveys` - List surveys with pagination and search
- `GET /api/surveys/{id}` - Get survey by ID
- `POST /api/surveys` - Create new survey
- `PUT /api/surveys/{id}` - Update survey
- `DELETE /api/surveys/{id}` - Delete survey

### Properties
- `GET /api/properties` - List properties with pagination and search
- `GET /api/properties/{id}` - Get property by ID
- `POST /api/properties` - Create new property
- `PUT /api/properties/{id}` - Update property
- `DELETE /api/properties/{id}` - Delete property

### Lookup Data
- `GET /api/lookup/survey-types` - Get survey types
- `GET /api/lookup/survey-statuses` - Get survey statuses
- `GET /api/lookup/townships` - Get townships

## Development

### Adding New Features

1. **Backend**: Add new routes in `routers/`, update models in `models.py`, and CRUD operations in `crud.py`
2. **Frontend**: Create new components in `components/`, pages in `pages/`, and update types in `types.ts`

### Database Changes

1. Update the SQL schema in `Database Scripts/schema.sql`
2. Update SQLAlchemy models in `backend/models.py`
3. Update Pydantic schemas in `backend/schemas.py`
4. Update TypeScript types in `frontend/src/types.ts`

## Production Deployment

### Backend
- Configure production database connection
- Set proper CORS origins
- Use a production WSGI server like Gunicorn
- Set up environment variables securely

### Frontend
- Build the production bundle: `npm run build`
- Serve static files with a web server like Nginx
- Configure API URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
