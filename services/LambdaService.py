from botocore.exceptions import ClientError


class LambdaService:
    """LambdaService class provides methods to interact with AWS Lambda.

    It allows you to create Lambda functions and invoke them with payloads.
    """
    def __init__(self, lambda_client):
        """Initialize the LambdaService with a boto3 Lambda client.

        Args:
            lambda_client: A boto3 Lambda client instance.
        """
        self.lambda_client = lambda_client

    def create_lambda_function(self, function_name, runtime, role_arn, handler, code):
        """Create a new Lambda function.

        Args:
            function_name (str): The name of the Lambda function to create.
            runtime (str): The runtime environment (e.g., 'python3.9', 'nodejs14.x').
            role_arn (str): The ARN of the IAM role to associate with the function.
            handler (str): The handler to invoke (e.g., 'index.handler').
            code (dict): A dictionary containing the code location (S3 bucket, key, or ZipFile).

        Returns:
            dict: The response from the create_function API call, or None if an error occurs.
        """
        try:
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=handler,
                Code=code
            )
            return response
        except ClientError as e:
            print(f"Error creating Lambda function: {e}")
            return None

    def invoke_lambda_function(self, function_name, payload):
        """Invoke a Lambda function with a payload.

        Args:
            function_name (str): The name of the Lambda function to invoke.
            payload (str or bytes): The input payload for the Lambda function.

        Returns:
            dict: The response from the invoke API call, or None if an error occurs.
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                Payload=payload
            )
            return response
        except ClientError as e:
            print(f"Error invoking Lambda function: {e}")
            return None