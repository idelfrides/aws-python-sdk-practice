from botocore.exceptions import ClientError


class CloudFrontService:
    def __init__(self, cloudfront_client):
        self.cloudfront_client = cloudfront_client
    
    def list_distributions(self):
        try:
            response = self.cloudfront_client.list_distributions()
            distributions = response.get('DistributionList', {}).get('Items', [])
            print(f"CloudFront Distributions: {distributions}")
            return distributions
        except ClientError as e:
            print(f"Error listing CloudFront distributions: {e}")
            return []
    
    def get_distribution(self, distribution_id):
        try:
            response = self.cloudfront_client.get_distribution(Id=distribution_id)
            distribution = response.get('Distribution', {})
            print(f"CloudFront Distribution {distribution_id}: {distribution}")
            return distribution
        except ClientError as e:
            print(f"Error getting CloudFront distribution: {e}")
            return None
    
    def create_distribution(self, distribution_config):
        try:
            response = self.cloudfront_client.create_distribution(DistributionConfig=distribution_config)
            distribution = response.get('Distribution', {})
            print(f"Created CloudFront Distribution: {distribution}")
            return distribution
        except ClientError as e:
            print(f"Error creating CloudFront distribution: {e}")
            return None
        
    def delete_distribution(self, distribution_id):
        try:
            # First, get the distribution to find the ETag
            distribution = self.get_distribution(distribution_id)
            if not distribution:
                print(f"Distribution {distribution_id} not found")
                return False
            
            etag = distribution.get('ETag')
            if not etag:
                print(f"ETag not found for distribution {distribution_id}")
                return False
            
            self.cloudfront_client.delete_distribution(Id=distribution_id, IfMatch=etag)
            print(f"Deleted CloudFront Distribution {distribution_id}")
            return True
        except ClientError as e:
            print(f"Error deleting CloudFront distribution: {e}")
            return False
        
    def update_distribution(self, distribution_id, distribution_config):
        try:
            # First, get the distribution to find the ETag
            distribution = self.get_distribution(distribution_id)
            if not distribution:
                print(f"Distribution {distribution_id} not found")
                return None
            
            etag = distribution.get('ETag')
            if not etag:
                print(f"ETag not found for distribution {distribution_id}")
                return None
            
            response = self.cloudfront_client.update_distribution(
                Id=distribution_id,
                IfMatch=etag,
                DistributionConfig=distribution_config
            )
            updated_distribution = response.get('Distribution', {})
            print(f"Updated CloudFront Distribution: {updated_distribution}")
            return updated_distribution
        except ClientError as e:
            print(f"Error updating CloudFront distribution: {e}")
            return None