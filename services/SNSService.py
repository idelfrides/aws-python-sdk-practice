class SNSService:
    """SNSService class provides methods to interact with AWS SNS (Simple Notification Service).

    It allows you to create topics, subscribe email addresses to topics, and publish messages to topics.
    """
    
    def __init__(self, sns_client):
        """
        Initialize the SNSService with a boto3 SNS client.
        """       
        self.sns_client = sns_client

    def create_topic(self, topic_name):
        """Create an SNS topic.

        Args:
            topic_name (str): The name of the SNS topic to create.

        Returns:
            str: The ARN (Amazon Resource Name) of the created topic.
        """
        response = self.sns_client.create_topic(Name=topic_name)
        return response['TopicArn']

    def subscribe_email(self, topic_arn, email_address):
        """Subscribe an email address to an SNS topic.

        Args:
            topic_arn (str): The ARN of the SNS topic.
            email_address (str): The email address to subscribe to the topic.

        Returns:
            str: The ARN of the subscription.
        """
        response = self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        return response['SubscriptionArn']

    def publish_message(self, topic_arn, message, subject=None):
        """Publish a message to an SNS topic.

        Args:
            topic_arn (str): The ARN of the SNS topic.
            message (str): The message to publish.
            subject (str, optional): The subject line for email messages. Defaults to None.

        Returns:
            str: The MessageId of the published message.
        """
        publish_params = {
            'TopicArn': topic_arn,
            'Message': message
        }
        if subject:
            publish_params['Subject'] = subject
        
        response = self.sns_client.publish(**publish_params)
        return response['MessageId']