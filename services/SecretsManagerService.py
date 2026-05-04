from botocore.exceptions import ClientError


class SecretsManagerService:
    
    def __init__(self, secrets_manager_client):
        self.secrets_manager_client = secrets_manager_client
    
    def get_secret(self, secret_name):
        try:
            response = self.secrets_manager_client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except ClientError as e:
            print(f"Error retrieving secret: {e}")
            return None 
        
    def create_secret(self, secret_name, secret_value):
        try:
            self.secrets_manager_client.create_secret(Name=secret_name, SecretString=secret_value)
            print(f"Secret {secret_name} created successfully")
        except ClientError as e:
            print(f"Error creating secret: {e}")
            
    def delete_secret(self, secret_name):   
        try:
            self.secrets_manager_client.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
            print(f"Secret {secret_name} deleted successfully")
        except ClientError as e:
            print(f"Error deleting secret: {e}")
            
    def secret_exists(self, secret_name):
        try:
            self.secrets_manager_client.describe_secret(SecretId=secret_name)
            return True
        except ClientError as e:
            print(f"Secret {secret_name} does not exist: {e}")
            return False  
        
    def list_secrets(self):
        try:
            response = self.secrets_manager_client.list_secrets()
            secrets = [secret['Name'] for secret in response['SecretList']]
            print(f"Secrets: {secrets}")
            return secrets
        except ClientError as e:
            print(f"Error listing secrets: {e}")
            return []
         
        
    