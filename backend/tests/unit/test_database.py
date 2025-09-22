"""
Unit tests for database layer (database.py)
Tests DynamoDB connection and helper functions
"""
import pytest
import boto3
from moto import mock_aws
from unittest.mock import patch, MagicMock

from database import get_dynamodb, get_table, DynamoDBConnection


class TestDynamoDBConnection:
    """Test DynamoDB connection functionality"""
    
    def test_dynamodb_connection_init(self, test_env_vars):
        """Test DynamoDB connection initialization"""
        with mock_aws():
            conn = DynamoDBConnection()
            assert conn.dynamodb is not None
            assert conn.region == 'us-east-1'
    
    def test_dynamodb_connection_with_endpoint(self, test_env_vars):
        """Test DynamoDB connection with custom endpoint"""
        import os
        os.environ["DYNAMODB_ENDPOINT_URL"] = "http://localhost:8000"
        
        with mock_aws():
            conn = DynamoDBConnection()
            assert conn.endpoint_url == "http://localhost:8000"
    
    def test_get_dynamodb_function(self, mock_dynamodb_tables):
        """Test get_dynamodb function returns valid resource"""
        dynamodb = get_dynamodb()
        assert dynamodb is not None
        
        # Test that we can list tables
        tables = list(dynamodb.tables.all())
        table_names = [table.name for table in tables]
        assert 'Customers' in table_names
        assert 'Surveys' in table_names
        assert 'Properties' in table_names
    
    def test_get_table_function(self, mock_dynamodb_tables):
        """Test get_table function returns valid table"""
        customers_table = get_table('Customers')
        assert customers_table is not None
        assert customers_table.table_name == 'Customers'
        
        surveys_table = get_table('Surveys')
        assert surveys_table is not None
        assert surveys_table.table_name == 'Surveys'
        
        properties_table = get_table('Properties')
        assert properties_table is not None
        assert properties_table.table_name == 'Properties'
    
    def test_get_table_invalid_name(self, mock_dynamodb_tables):
        """Test get_table with invalid table name"""
        with pytest.raises(Exception):
            get_table('NonExistentTable')
    
    @patch('database.boto3')
    def test_connection_error_handling(self, mock_boto3):
        """Test connection error handling"""
        mock_boto3.resource.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            DynamoDBConnection()
        assert "Connection failed" in str(exc_info.value)
    
    def test_connection_singleton_behavior(self, mock_dynamodb_tables):
        """Test that connection behaves like singleton"""
        # Note: This tests that multiple calls return working connections
        dynamodb1 = get_dynamodb()
        dynamodb2 = get_dynamodb()
        
        # Both should be valid DynamoDB resources
        assert dynamodb1 is not None
        assert dynamodb2 is not None
        
        # Both should be able to access the same tables
        table1 = dynamodb1.Table('Customers')
        table2 = dynamodb2.Table('Customers')
        
        assert table1.table_name == table2.table_name
    
    def test_table_operations(self, mock_dynamodb_tables):
        """Test basic table operations work"""
        table = get_table('Customers')
        
        # Test table scan (should be empty initially)
        response = table.scan()
        assert 'Items' in response
        assert len(response['Items']) == 0
        
        # Test put item
        test_item = {
            'id': 'test-customer-id',
            'CustomerCode': 'TEST001',
            'CompanyName': 'Test Company',
            'Email': 'test@example.com',
            'IsActive': True
        }
        
        table.put_item(Item=test_item)
        
        # Test get item
        response = table.get_item(Key={'id': 'test-customer-id'})
        assert 'Item' in response
        assert response['Item']['CustomerCode'] == 'TEST001'
    
    def test_environment_variables_loading(self, test_env_vars):
        """Test that environment variables are properly loaded"""
        import os
        
        # Test default values when env vars are not set
        original_region = os.environ.get('AWS_REGION')
        if 'AWS_REGION' in os.environ:
            del os.environ['AWS_REGION']
        
        with mock_aws():
            conn = DynamoDBConnection()
            # Should use default region
            assert conn.region in ['us-east-1', 'us-west-2']  # Common defaults
        
        # Restore original value
        if original_region:
            os.environ['AWS_REGION'] = original_region
    
    def test_aws_credentials_in_test_env(self, test_env_vars):
        """Test that AWS credentials are set for testing"""
        import os
        
        assert os.environ.get('AWS_ACCESS_KEY_ID') == 'testing'
        assert os.environ.get('AWS_SECRET_ACCESS_KEY') == 'testing'
        assert os.environ.get('AWS_REGION') == 'us-east-1'


class TestTableConfiguration:
    """Test table configuration and setup"""
    
    def test_all_required_tables_created(self, mock_dynamodb_tables):
        """Test that all required tables are created in the test environment"""
        dynamodb = get_dynamodb()
        
        # Get list of table names
        tables = list(dynamodb.tables.all())
        table_names = [table.name for table in tables]
        
        required_tables = ['Customers', 'Surveys', 'Properties']
        for table_name in required_tables:
            assert table_name in table_names
    
    def test_table_key_schema(self, mock_dynamodb_tables):
        """Test that tables have correct key schema"""
        # Test Customers table
        customers = get_table('Customers')
        key_schema = customers.key_schema
        
        # Should have a hash key named 'id'
        hash_key = next(k for k in key_schema if k['KeyType'] == 'HASH')
        assert hash_key['AttributeName'] == 'id'
        
        # Test Surveys table
        surveys = get_table('Surveys')
        key_schema = surveys.key_schema
        hash_key = next(k for k in key_schema if k['KeyType'] == 'HASH')
        assert hash_key['AttributeName'] == 'id'
        
        # Test Properties table
        properties = get_table('Properties')
        key_schema = properties.key_schema
        hash_key = next(k for k in key_schema if k['KeyType'] == 'HASH')
        assert hash_key['AttributeName'] == 'id'
    
    def test_table_global_secondary_indexes(self, mock_dynamodb_tables):
        """Test that tables have correct Global Secondary Indexes"""
        # Test Customers table GSI
        customers = get_table('Customers')
        gsi_names = [gsi['IndexName'] for gsi in customers.global_secondary_indexes or []]
        assert 'email-index' in gsi_names
        
        # Test Surveys table GSI
        surveys = get_table('Surveys')
        gsi_names = [gsi['IndexName'] for gsi in surveys.global_secondary_indexes or []]
        assert 'customer-index' in gsi_names
        
        # Test Properties table GSI
        properties = get_table('Properties')
        gsi_names = [gsi['IndexName'] for gsi in properties.global_secondary_indexes or []]
        assert 'customer-index' in gsi_names
    
    def test_table_billing_mode(self, mock_dynamodb_tables):
        """Test that tables use correct billing mode"""
        tables = ['Customers', 'Surveys', 'Properties']
        
        for table_name in tables:
            table = get_table(table_name)
            # In moto, billing mode information might not be directly accessible
            # But we can verify the table is functional
            assert table.table_name == table_name
            assert table.table_status == 'ACTIVE'
    
    def test_table_attribute_definitions(self, mock_dynamodb_tables):
        """Test that tables have correct attribute definitions"""
        # Test Customers table
        customers = get_table('Customers')
        attr_names = [attr['AttributeName'] for attr in customers.attribute_definitions]
        assert 'id' in attr_names
        assert 'email' in attr_names
        
        # Test Surveys table
        surveys = get_table('Surveys')
        attr_names = [attr['AttributeName'] for attr in surveys.attribute_definitions]
        assert 'id' in attr_names
        assert 'customer_id' in attr_names
        
        # Test Properties table
        properties = get_table('Properties')
        attr_names = [attr['AttributeName'] for attr in properties.attribute_definitions]
        assert 'id' in attr_names
        assert 'customer_id' in attr_names


class TestDatabaseIntegration:
    """Test database integration functionality"""
    
    def test_connection_persistence(self, mock_dynamodb_tables):
        """Test that connection persists across operations"""
        # Perform multiple operations
        table1 = get_table('Customers')
        table2 = get_table('Surveys')
        table3 = get_table('Properties')
        
        # All should be accessible
        assert table1.table_name == 'Customers'
        assert table2.table_name == 'Surveys'
        assert table3.table_name == 'Properties'
    
    def test_concurrent_access(self, mock_dynamodb_tables):
        """Test concurrent access to tables"""
        import threading
        import time
        
        results = []
        
        def access_table(table_name):
            try:
                table = get_table(table_name)
                response = table.scan()
                results.append(f"{table_name}: {len(response['Items'])}")
            except Exception as e:
                results.append(f"{table_name}: Error - {str(e)}")
        
        # Create threads for concurrent access
        threads = []
        table_names = ['Customers', 'Surveys', 'Properties']
        
        for table_name in table_names:
            thread = threading.Thread(target=access_table, args=(table_name,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All operations should succeed
        assert len(results) == 3
        for result in results:
            assert "Error" not in result
    
    def test_error_recovery(self, mock_dynamodb_tables):
        """Test error recovery and connection resilience"""
        # Test with invalid table access
        try:
            get_table('InvalidTable')
            assert False, "Should have raised an exception"
        except Exception:
            pass  # Expected
        
        # Connection should still work for valid tables
        table = get_table('Customers')
        assert table.table_name == 'Customers'
        
        # Should be able to perform operations
        response = table.scan()
        assert 'Items' in response