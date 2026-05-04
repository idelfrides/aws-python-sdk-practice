
from services import LambdaService, SNSService, SQSService
from services.S3Service import S3Service


class ConfigurationServices:
        
    def __init__(self, lambda_client, sqs_client, sns_client, s3_client):
        self.lambda_service = LambdaService(lambda_client)
        self.sqs_service = SQSService(sqs_client)
        self.sns_service = SNSService(sns_client)
        self.s3_service = S3Service(s3_client)
