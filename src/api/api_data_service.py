import pandas as pd
import requests
from botocore.exceptions import ClientError


class ApiDataService:
    """
    Service for fetching API data and saving it to storage or returning as a DataFrame.
    Works with an API client (e.g., UnstableAPIClient) and StorageDataService.
    """

    def __init__(self, api_client, storage_service, logger):
        """
        Args:
            api_client: Instance of UnstableAPIClient or other API client.
            storage_service: Instance of StorageDataService.
            logger: Logger instance.
        """
        self.api_client = api_client
        self.storage = storage_service
        self.logger = logger

    def fetch_all_to_df(self, limit=1000):
        """
        Fetch all pages from the API and return as a single DataFrame.

        Args:
            limit (int): Number of records per page.

        Returns:
            pd.DataFrame
        """
        frames = []
        try:
            for page, result in self.api_client.iterate_all_pages(limit=limit):
                if result and "data" in result:
                    frames.append(pd.DataFrame(result["data"]))
                else:
                    self.logger.warning(f"Page {page} returned no data.")
        except (requests.RequestException, pd.errors.EmptyDataError, ValueError) as e:
            self.logger.error(f"Error fetching API data: {e}", exc_info=True)

        if frames:
            try:
                return pd.concat(frames, ignore_index=True)
            except ValueError as e:
                # e.g., if frames list contains empty DataFrames
                self.logger.error(f"Error concatenating DataFrames: {e}", exc_info=True)
                return pd.DataFrame()
        else:
            self.logger.warning("No data fetched from API.")
            return pd.DataFrame()

    def fetch_all_to_storage(self, bucket, key, format="csv", limit=1000):
        """
        Fetch all API data and upload it to storage in the requested format.

        Args:
            bucket (str): Storage bucket name.
            key (str): Object path in storage.
            format (str): "csv", "json", or "parquet".
            limit (int): Number of records per page.
        """
        try:
            df = self.fetch_all_to_df(limit=limit)
        except (requests.RequestException, pd.errors.EmptyDataError, ValueError) as e:
            self.logger.error(f"Failed to fetch API data: {e}", exc_info=True)
            return

        if df.empty:
            self.logger.warning("No data to upload to storage.")
            return

        try:
            self.storage.upload_df(df, bucket=bucket, key=key, format=format)
            self.logger.info(f"Uploaded API data to {bucket}/{key} as {format}.")
        except (ValueError, ClientError) as e:
            self.logger.error(f"Failed to upload data to storage: {e}", exc_info=True)
