import requests
import json


class LambdaResponseTriggerService:
    def __init__(self, lambda_client):
        self.lambda_client = lambda_client

    def trigger_lambda_function(self, function_name, payload):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='Event',  # Asynchronous invocation
            Payload=payload
        )
        return response
    
    def api_getway_response(self, api_url):               
         
        get_response = requests.get(api_url)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'get_response': get_response.json()
            })
        }
        