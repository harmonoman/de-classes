from botocore.exceptions import ClientError
from src.storage.clients.base_s3_client import BaseS3Client


class MinioClient(BaseS3Client):
    """
    A MinIO-specific S3 client built on top of BaseS3Client.

    Provides convenience defaults and helper utilities for local MinIO setups.
    """
    def __init__(
        self,
        logger,
        endpoint_url="http://localhost:9000",
        access_key=None,
        secret_key=None,
        region_name="us-east-1",
    ):
        """
        Create a MinIO client with MinIO-friendly defaults.
        """
        super().__init__(
            logger=logger,
            endpoint_url=endpoint_url,
            access_key=access_key,
            secret_key=secret_key,
            region_name=region_name,
        )

    def ensure_bucket(self, bucket):
        """
        Create the bucket if it does not already exist.
        MinIO requires buckets to be created explicitly.
        """
        try:
            self.s3.head_bucket(Bucket=bucket)
            return True
        except ClientError:
            # Try to create it
            try:
                self.s3.create_bucket(Bucket=bucket)
                self.logger.info(f"Bucket '{bucket}' created in MinIO.")
                return True
            except ClientError as e:
                self.logger.error(f"Failed to create bucket '{bucket}': {e}", exc_info=True)
                raise
