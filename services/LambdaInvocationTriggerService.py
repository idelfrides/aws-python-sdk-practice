import requests
import json


class LambdaInvocationTriggerService:
    def __init__(self, lambda_client):
        self.lambda_client = lambda_client

    def trigger_lambda_function(self, function_name, payload):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='Event',  # Asynchronous invocation
            Payload=payload
        )
        return response
    
    def api_getway_trigger_lambda(self, api_url):               
        
        payload = {"test_name": "it-sessions-api-gateway", "message": "Hello from API Gateway!"}
        headers = {'Content-Type': 'application/json'}        
        
        post_response = requests.post(api_url, json=payload, headers=headers)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'post_response': post_response.json(),
            })
        }
        