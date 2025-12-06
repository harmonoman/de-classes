from src.storage.clients.s3_client import S3Client
from src.storage.clients.minio_client import MinioClient
from src.storage.services.storage_data_service import StorageDataService
from src.storage.format.data_format_service import DataFormatService
import pandas as pd


def test_storage(logger):
    # --- Create a sample DataFrame ---
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })

    # --- Choose client ---
    # Example: MinIO (local or configured)
    storage_client = MinioClient(
        logger=logger,
        endpoint_url="http://localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin"
    )
    storage_client.ensure_bucket("test-bucket")

    # --- Create StorageDataService ---
    fmt_service = DataFormatService()
    storage_service = StorageDataService(storage_client, fmt_service, logger)

    # --- Upload DataFrame ---
    storage_service.upload_df(df, bucket="test-bucket", key="sample.csv", format="csv")
    print("Upload successful!")

    # --- Download DataFrame ---
    df_downloaded = storage_service.download_df(bucket="test-bucket", key="sample.csv", format="csv")
    print("Downloaded DataFrame:")
    print(df_downloaded)
