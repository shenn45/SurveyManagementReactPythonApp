# Survey Management API

FastAPI backend for the Survey Management System.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your database connection:
```
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

5. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`
