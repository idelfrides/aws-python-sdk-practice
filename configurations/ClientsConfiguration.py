
from tkinter import constants


class ClientsConfiguration:
        
    def __init__(self, lambda_client, sqs_client, sns_client, s3_client, secrets_manager_client, cloudfront_client):
        self.lambda_client = lambda_client
        self.sqs_client = sqs_client
        self.sns_client = sns_client
        self.s3_client = s3_client
        self.secrets_manager_client = secrets_manager_client
        self.cloudfront_client = cloudfront_client