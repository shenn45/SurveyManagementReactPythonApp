#!/bin/bash

echo "🚀 Setting up Survey Management Application..."

# Backend setup
echo "📦 Setting up Python backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    ./venv/Scripts/activate
    pip install -r requirements.txt
else
    # Linux/Mac
    source venv/bin/activate
    pip install -r requirements.txt
fi

echo "✅ Backend setup complete!"

# Frontend setup
echo "📦 Setting up React frontend..."
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your database connection in backend/.env"
echo "2. Run the database schema from Database Scripts/schema.sql"
echo "3. Start the backend: cd backend && uvicorn main:app --reload"
echo "4. Start the frontend: cd frontend && npm start"
