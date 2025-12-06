import boto3
from src.storage.clients.base_s3_client import BaseS3Client


class S3Client(BaseS3Client):
    """
    AWS S3 client using default AWS credentials or explicit keys.
    """
    def __init__(
        self,
        logger,
        access_key=None,
        secret_key=None,
        region_name="us-east-1",
        session_profile=None,
    ):
        """
        Create an AWS S3 client.

        Parameters
        ----------
        logger : Logger
            Logger instance.
        access_key : str, optional
            AWS access key.
        secret_key : str, optional
            AWS secret key.
        region_name : str
            AWS region.
        session_profile : str, optional
            AWS CLI profile name.
        """

        if session_profile:
            session = boto3.Session(profile_name=session_profile)
            s3_client = session.client("s3", region_name=region_name)
        elif access_key and secret_key:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name,
            )
        else:
            # Default credentials (IAM role, env vars, ~/.aws/)
            s3_client = boto3.client("s3", region_name=region_name)

        self.logger = logger
        self.s3 = s3_client

    # OPTIONAL AWS extras
    def list_buckets(self):
        """Return all S3 buckets for the authenticated account."""
        response = self.s3.list_buckets()
        return [b["Name"] for b in response.get("Buckets", [])]

    def enable_bucket_versioning(self, bucket):
        """Turn on versioning for a bucket."""
        self.s3.put_bucket_versioning(
            Bucket=bucket,
            VersioningConfiguration={"Status": "Enabled"},
        )

    def get_object_version(self, bucket, key):
        """Get version ID of an S3 object."""
        obj = self.s3.head_object(Bucket=bucket, Key=key)
        return obj.get("VersionId")
