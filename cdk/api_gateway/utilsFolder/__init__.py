""" Util Functions for Lambda Test Cases

    This module contains utility functions for testing Lambda functions. Originally,
    it was developed to standardize the way we create the mock AWS services for
    our lambda test cases. These functions should be used in test cases that use the
    moto decorators.

    Functions:

        create_test_users_table() - Creates a DynamoDB table that mocks the users
            table.

        create_test_visit_table() - Creates a DynamoDB table that mocks the visits
            table.

        create_original_table() - Creates a DynamoDB table that mocks the original
            table.

        create_ses_client() - Creates a mock SES client. 
        
    
    

"""
