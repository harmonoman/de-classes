import boto3
from botocore.exceptions import ClientError


class BaseS3Client:
    """
    A minimal, generic S3-compatible client for interacting with object
    storage systems such as AWS S3 or MinIO using the boto3 API.

    This client provides low-level byte-oriented operations (upload, download,
    exists) and is intended to be extended by more specialized clients.
    """

    def __init__(self, logger, endpoint_url, access_key, secret_key, region_name="us-east-1"):
        """
        Create an S3 client.
        """
        self.logger = logger
        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name
        )

    def upload_bytes(self, bucket, key, data, content_type="text/csv"):
        """ Upload raw bytes to the given bucket/key."""
        try:
            self.s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
            self.logger.info(f"Uploaded {key} to bucket {bucket}")
        except ClientError as e:
            self.logger.error(f"Failed to upload {key} to bucket {bucket}: {e}", exc_info=True)
            raise

    def download_bytes(self, bucket, key):
        """ Download the object and return its raw bytes."""
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=key)
            return obj["Body"].read()
        except ClientError as e:
            self.logger.error(f"Failed to download {key} from bucket {bucket}: {e}", exc_info=True)
            raise

    def exists(self, bucket, key):
        """ Return True if the object exists, otherwise False."""
        try:
            self.s3.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            self.logger.error(f"Error checking existence of {key} in {bucket}: {e}", exc_info=True)
            raise
