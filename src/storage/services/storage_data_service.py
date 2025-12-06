class StorageDataService:
    """
    Service for uploading and downloading pandas DataFrames
    to/from storage systems like S3 or MinIO.
    Handles the serialization/deserialization (CSV, JSON, Parquet).
    """
    def __init__(self, storage_client, format_service, logger):
        """
        Args:
            storage_client: S3Client or MinioClient instance.
            format_service: DataFormatService for format conversions.
            logger: Logger for messages and errors.
        """
        self.storage = storage_client        # S3Client or MinioClient
        self.fmt = format_service            # DataFormatService
        self.logger = logger

    def upload_df(self, df, bucket, key, format="csv"):
        """
        Serialize a DataFrame and upload it.

        Args:
            df (pd.DataFrame): Data to upload.
            bucket (str): Bucket name.
            key (str): Object path.
            format (str): "csv", "json", or "parquet".

        Raises:
            ValueError: Unsupported format.
        """
        if format == "csv":
            data = self.fmt.df_to_csv_bytes(df)
        elif format == "json":
            data = self.fmt.df_to_json_bytes(df)
        elif format == "parquet":
            data = self.fmt.df_to_parquet_bytes(df)
        else:
            raise ValueError(f"Unsupported format: {format}")

        self.storage.upload_bytes(bucket, key, data)

    def download_df(self, bucket, key, format="csv"):
        """
        Download an object and return it as a DataFrame.

        Args:
            bucket (str): Bucket name.
            key (str): Object path.
            format (str): Expected format.

        Returns:
            pd.DataFrame
        """
        data = self.storage.download_bytes(bucket, key)

        if format == "csv":
            return self.fmt.csv_bytes_to_df(data)
        elif format == "json":
            return self.fmt.json_bytes_to_df(data)
        elif format == "parquet":
            return self.fmt.parquet_bytes_to_df(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
