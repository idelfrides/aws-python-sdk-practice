from botocore.exceptions import ClientError


class S3Service:
    def __init__(self, s3_client):
        self.s3_client = s3_client

    def upload_file(self, file_path, bucket_name, object_name):
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    def download_file(self, bucket_name, object_name, file_path):
        try:
            self.s3_client.download_file(bucket_name, object_name, file_path)
            print(f"File {object_name} downloaded from {bucket_name} to {file_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")

    def delete_file(self, bucket_name, object_name):
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_name)
            print(f"File {object_name} deleted from {bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")
    
    def list_files(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                files = [obj['Key'] for obj in response['Contents']]
                print(f"Files in {bucket_name}: {files}")
                return files
            else:
                print(f"No files found in {bucket_name}")
                return []
        except ClientError as e:
            print(f"Error listing files: {e}")
            return []
    
    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} created successfully")
        except ClientError as e:
            print(f"Error creating bucket: {e}")
            
    def delete_bucket(self, bucket_name):
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} deleted successfully")
        except ClientError as e:
            print(f"Error deleting bucket: {e}")
    
    def bucket_exists(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            print(f"Bucket {bucket_name} does not exist: {e}")
            return False
        
    def file_exists(self, bucket_name, object_name):
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=object_name)
            return True
        except ClientError as e:
            print(f"File {object_name} does not exist in {bucket_name}: {e}")
            return False    
        
    def get_file_url(self, bucket_name, object_name):
        try:
            url = self.s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=3600)
            print(f"Presigned URL for {object_name} in {bucket_name}: {url}")
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
        
    def copy_file(self, source_bucket_name, source_object_name, destination_bucket_name, destination_object_name):
        try:
            copy_source = {'Bucket': source_bucket_name, 'Key': source_object_name}
            self.s3_client.copy(copy_source, destination_bucket_name, destination_object_name)
            print(f"File {source_object_name} copied from {source_bucket_name} to {destination_bucket_name}/{destination_object_name}")
        except ClientError as e:
            print(f"Error copying file: {e}")
            
    def move_file(self, source_bucket_name, source_object_name, destination_bucket_name, destination_object_name):
        try:
            self.copy_file(source_bucket_name, source_object_name, destination_bucket_name, destination_object_name)
            self.delete_file(source_bucket_name, source_object_name)
            print(f"File {source_object_name} moved from {source_bucket_name} to {destination_bucket_name}/{destination_object_name}")
        except ClientError as e:
            print(f"Error moving file: {e}")
    
    def get_file_metadata(self, bucket_name, object_name):
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_name)
            metadata = response['Metadata']
            print(f"Metadata for {object_name} in {bucket_name}: {metadata}")
            return metadata
        except ClientError as e:
            print(f"Error getting file metadata: {e}")
            return None
        
    def set_file_metadata(self, bucket_name, object_name, metadata):
        try:
            copy_source = {'Bucket': bucket_name, 'Key': object_name}
            self.s3_client.copy(copy_source, bucket_name, object_name, ExtraArgs={'Metadata': metadata, 'MetadataDirective': 'REPLACE'})
            print(f"Metadata for {object_name} in {bucket_name} updated to: {metadata}")
        except ClientError as e:
            print(f"Error setting file metadata: {e}")
    
    def create_folder(self, bucket_name, folder_name):
        try:
            self.s3_client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))
            print(f"Folder {folder_name} created in {bucket_name}")
        except ClientError as e:
            print(f"Error creating folder: {e}")
            
    