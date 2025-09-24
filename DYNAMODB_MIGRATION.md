# DynamoDB Migration Guide

This document outlines the migration from MSSQL to Amazon DynamoDB for the Survey Management application.

## Overview

The application has been updated to use Amazon DynamoDB instead of MSSQL as the primary database. This change provides:

- **Scalability**: DynamoDB automatically scales based on demand
- **Performance**: Consistent single-digit millisecond response times
- **Serverless**: No database servers to manage
- **Global**: Multi-region replication capabilities
- **Cost-effective**: Pay-per-request pricing model

## Key Changes

### 1. Database Layer (`database.py`)
- Replaced SQLAlchemy with boto3 DynamoDB client
- Implemented connection management for DynamoDB
- Added support for local DynamoDB development

### 2. Data Models (`models.py`)
- Converted SQLAlchemy models to Pydantic models
- Changed primary keys from auto-incrementing integers to UUIDs
- Added DynamoDB table configuration with Global Secondary Indexes
- Removed foreign key relationships (DynamoDB is NoSQL)

### 3. CRUD Operations (`crud.py`)
- Replaced SQL queries with DynamoDB operations
- Implemented proper serialization/deserialization for DynamoDB
- Added error handling for DynamoDB-specific exceptions
- Updated function signatures to remove database session dependencies

### 4. Dependencies (`requirements.txt`)
- Removed SQLAlchemy, pyodbc, and alembic
- Added boto3 and botocore for DynamoDB access
- Kept FastAPI, GraphQL, and other non-database dependencies

### 5. API Routes
- Updated router files to remove database session dependencies
- Changed ID parameters from integers to strings (UUIDs)
- Simplified dependency injection

## Setup Instructions

### Prerequisites
1. AWS Account (for production) or Docker (for local development)
2. Python 3.13.7+ environment
3. Required Python packages (see requirements.txt)

### AWS Configuration

#### Option 1: AWS Credentials File
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

#### Option 2: Environment Variables
Set the following environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

#### Option 3: Environment File
Copy `.env.dynamodb` to `.env` and update with your credentials:
```bash
cp .env.dynamodb .env
# Edit .env with your AWS credentials
```

### Local Development with DynamoDB Local

For local development, you can use DynamoDB Local with Docker:

```bash
# Start DynamoDB Local
docker run -p 8001:8001 amazon/dynamodb-local

# Set environment variable
export DYNAMODB_ENDPOINT_URL=http://localhost:8001
```

### Database Table Creation

Create all required DynamoDB tables:

```bash
# Install dependencies
pip install -r requirements.txt

# Create tables
python create_tables.py create

# List existing tables
python create_tables.py list

# Delete all tables (use with caution!)
python create_tables.py delete
```

### Running the Application

```bash
# Start the FastAPI server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## DynamoDB Table Structure

### Tables Created

1. **Customers** - Customer information
   - Primary Key: `CustomerId` (String/UUID)
   - GSI: `CustomerCodeIndex`, `CompanyNameIndex`

2. **Addresses** - Address information
   - Primary Key: `AddressId` (String/UUID)
   - GSI: `AddressTypeIndex`

3. **Properties** - Property information
   - Primary Key: `PropertyId` (String/UUID)
   - GSI: `PropertyCodeIndex`

4. **Surveys** - Survey records
   - Primary Key: `SurveyId` (String/UUID)
   - GSI: `SurveyNumberIndex`, `CustomerIdIndex`

5. **SurveyTypes** - Survey type lookup
   - Primary Key: `SurveyTypeId` (String/UUID)

6. **SurveyStatuses** - Survey status lookup
   - Primary Key: `SurveyStatusId` (String/UUID)

7. **Townships** - Township information
   - Primary Key: `TownshipId` (String/UUID)
   - GSI: `TownshipNameIndex`

8. **SurveyFiles** - Survey file attachments
   - Primary Key: `SurveyFileId` (String/UUID)
   - GSI: `SurveyIdIndex`

9. **Documents** - Document storage
   - Primary Key: `DocumentId` (String/UUID)

10. **CustomerAddresses** - Customer-Address relationships
    - Primary Key: `CustomerAddressId` (String/UUID)
    - GSI: `CustomerIdIndex`

## API Changes

### REST API
- All ID parameters changed from integers to strings (UUIDs)
- Removed database session dependencies
- Same endpoint structure and response formats

### GraphQL API
- Updated field types from `Int` to `String` for IDs
- Removed database session management
- Same query and mutation structure

## Performance Considerations

### Query Patterns
- Use primary keys for point lookups (fastest)
- Use Global Secondary Indexes for non-key queries
- Avoid scanning large tables - use filters when possible
- Consider pagination for large result sets

### Cost Optimization
- Use on-demand billing for variable workloads
- Consider provisioned capacity for predictable workloads
- Monitor read/write capacity usage
- Use DynamoDB auto-scaling

## Monitoring and Maintenance

### CloudWatch Metrics
Monitor these key metrics:
- Read/Write capacity utilization
- Throttled requests
- Error rates
- Item sizes

### Backup Strategy
- Enable point-in-time recovery
- Set up automated backups
- Test restore procedures

## Migration from Existing Data

If migrating from existing MSSQL data:

1. Export data from MSSQL to JSON/CSV
2. Transform data to match new UUID-based schema
3. Use DynamoDB batch operations for bulk import
4. Verify data integrity after migration

## Troubleshooting

### Common Issues

1. **Access Denied**
   - Check AWS credentials and permissions
   - Ensure DynamoDB access policies are correct

2. **Table Not Found**
   - Run table creation script
   - Check table names and regions

3. **Validation Errors**
   - Check data types (especially UUID strings)
   - Verify required fields are present

4. **Performance Issues**
   - Review query patterns
   - Check if you're using appropriate indexes
   - Monitor capacity utilization

## Development Tips

1. Use DynamoDB Local for development
2. Keep table schemas documented
3. Use consistent naming conventions
4. Monitor costs in production
5. Test backup and restore procedures

For more information, see:
- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [Boto3 DynamoDB Guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)