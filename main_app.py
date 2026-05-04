import boto3
from configurations.ClientsConfiguration import ClientsConfiguration
from configurations.ConstantsDefinition import ConstantsDefinition
from services import LambdaResponseTriggerService, SecretsManagerService
from services.LambdaInvocationTriggerService import LambdaInvocationTriggerService
from services.LambdaResponseTriggerService import LambdaResponseTriggerService
from services.LambdaService import LambdaService
from services.S3Service import S3Service
from services.SQSService import SQSService
from services.SNSService import SNSService


def run_main_app():
    print("THIS IS MAIN APP IN UBUNTU PYTHON PROJECT")
    
    constants = ConstantsDefinition()
    
    config_clients = ClientsConfiguration(
        lambda_client=boto3.client('lambda', region_name=constants.AWS_REGION),
        sqs_client=boto3.client('sqs', region_name=constants.AWS_REGION),
        sns_client=boto3.client('sns', region_name=constants.AWS_REGION),
        s3_client=boto3.client('s3', region_name=constants.AWS_REGION),
        secrets_manager_client=boto3.client(
            'secretsmanager', region_name=constants.AWS_REGION),
        cloudfront_client=boto3.client(
            'cloudfront', region_name=constants.AWS_REGION)
    )
    
    
    # -------------------------------------------------
    # Execute LambdaService
    # -------------------------------------------------
    lambda_service = LambdaService(config_clients.lambda_client)
    lambda_response = lambda_service.create_lambda_function(
        function_name='TestFunction',
        runtime='python3.9',
        role_arn='arn:aws:iam::123456789012:role/lambda-role',
        handler='lambda_function.lambda_handler',
        code={
            'ZipFile': b'fileb://function.zip'
        }
    )
    print(f"Lambda function creation response: {lambda_response}")
    
       # Execute Lambda with API Gateway trigger
    lambda_invocation_service = LambdaInvocationTriggerService(lambda_service)

    api_response = (
        lambda_invocation_service.api_getway_trigger_lambda(
            constants.API_GETWAY_URL
        )
    )
    print(f"API Gateway trigger response: {api_response}")
    
    
    # Execute Lambda with API Gateway response trigger
    lambda_response_service = LambdaResponseTriggerService(lambda_service)
    api_response = (
        lambda_response_service.api_getway_response(constants.API_GETWAY_URL)
    )
    print(f"API Gateway response trigger response: {api_response}")
    
        
    # -------------------------------------------------
    # Execute SQSService
    # -------------------------------------------------
    sqs_service = SQSService(config_clients.sqs_client)
    queue_url = sqs_service.create_queue('TestQueue')
    print(f"SQS queue URL: {queue_url}")
    
    # -----------------------------------------------
    # Execute SNSService
    # -----------------------------------------------
    sns_service = SNSService(config_clients.sns_client)
    topic_arn = sns_service.create_topic('TestTopic')
    print(f"SNS topic ARN: {topic_arn}")

    # Example of subscribing an email to the SNS topic
    subscription_arn = sns_service.subscribe_email(topic_arn, 'example@example.com')
    print(f"SNS subscription ARN: {subscription_arn}")
    
    # Example of publishing a message to the SNS topic
    message_id = sns_service.publish_message(topic_arn, 'Hello, this is a test message!', subject='Test Message')
    print(f"SNS published message ID: {message_id}")
    
    # ----------------------------------------------
    # Execute S3Service
    # ----------------------------------------------
    s3_service = S3Service(config_clients.s3_client)
    s3_service.create_bucket('TestBucket')
    s3_service.create_folder('TestBucket', 'TestFolder')
    
    # Check if bucket and file exist
    bucket_exists = s3_service.bucket_exists('TestBucket')
    print(f"Bucket exists: {bucket_exists}")
    file_exists = s3_service.file_exists('TestBucket', 'TestFolder/testfile.txt')
    print(f"File exists: {file_exists}")
    
    # Get file URL
    file_url = s3_service.get_file_url('TestBucket', 'TestFolder/testfile.txt')
    print(f"File URL: {file_url}")
    
    # Copy and move file
    s3_service.copy_file('TestBucket', 'TestFolder/testfile.txt', 'TestBucket', 'TestFolder/testfile_copy.txt')
    s3_service.move_file('TestBucket', 'TestFolder/testfile_copy.txt', 'TestBucket', 'TestFolder/testfile_moved.txt')
  
    # Get and set file metadata
    metadata = s3_service.get_file_metadata('TestBucket', 'TestFolder/testfile.txt')
    print(f"File metadata: {metadata}")
    s3_service.set_file_metadata('TestBucket', 'TestFolder/testfile.txt', {'key': 'value'})
    metadata = s3_service.get_file_metadata('TestBucket', 'TestFolder/testfile.txt')
    print(f"Updated file metadata: {metadata}")
    
    
    # ----------------------------------------------
    # Execute SecretsManagerService
    # ----------------------------------------------
    
    # secret_name = constants.AWS_SECRET_NAME
    secret_name = constants.MY_APPS_SECRET_NAME
    
    secrets_manager_service = SecretsManagerService(
        config_clients.secrets_manager_client
    )
    
    if secrets_manager_service.secret_exists(secret_name):
        secret_value = secrets_manager_service.get_secret(secret_name)
        print(f"Retrieved secret value: {secret_value}")
    else:
        secrets_manager_service.create_secret(
            secret_name, 'This is a test secret value')
        secret_value = secrets_manager_service.get_secret(secret_name)
        print(f"Retrieved secret value: {secret_value}")
       
    #  secrets_manager_service.delete_secret(constants.AWS_SECRET_NAME)
          
    
    
    
# ----------------------------------------------------
#           INITIALIZATION OF MAIN APP 
# ----------------------------------------------------
 
if __name__ == "__main__":
    run_main_app()