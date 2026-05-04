class SQSService:
    """SQSService class provides methods to interact with AWS SQS (Simple Queue Service).

    It allows you to create queues, send messages, receive messages, and delete messages from SQS queues.
    """
    
    def __init__(self, sqs_client):
        """Initialize the SQSService with a boto3 SQS client.

        Args:
            sqs_client: A boto3 SQS client instance.
        """
        self.sqs_client = sqs_client

    def create_queue(self, queue_name):
        """Create a new SQS queue.

        Args:
            queue_name (str): The name of the SQS queue to create.

        Returns:
            str: The URL of the created queue.
        """
        response = self.sqs_client.create_queue(QueueName=queue_name)
        return response['QueueUrl']

    def send_message(self, queue_url, message_body):
        """Send a message to an SQS queue.

        Args:
            queue_url (str): The URL of the SQS queue.
            message_body (str): The message body to send.

        Returns:
            str: The MessageId of the sent message.
        """
        response = self.sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
        return response['MessageId']

    def receive_messages(self, queue_url, max_number_of_messages=1):
        """Receive messages from an SQS queue.

        Args:
            queue_url (str): The URL of the SQS queue.
            max_number_of_messages (int, optional): The maximum number of messages to receive. Defaults to 1.

        Returns:
            list: A list of message dictionaries received from the queue.
        """
        response = self.sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=max_number_of_messages)
        return response.get('Messages', [])

    def delete_message(self, queue_url, receipt_handle):
        """Delete a message from an SQS queue.

        Args:
            queue_url (str): The URL of the SQS queue.
            receipt_handle (str): The receipt handle of the message to delete.
        """
        self.sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)