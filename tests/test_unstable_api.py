import pandas as pd
from src.api.auth_client import AuthClient
from src.api.unstable_api_client import UnstableAPIClient
from src.api.api_data_service import ApiDataService


# -------------------------------
# Mock Storage
# -------------------------------
class MockStorageService:
    def upload_df(self, df: pd.DataFrame, bucket: str, key: str, format="csv"):
        # Just log or print for testing
        print(f"[MockStorage] Uploading {len(df)} records to {bucket}/{key} as {format}")


# -------------------------------
# Test case
# -------------------------------
def test_unstable_api_integration(logger):

    # AuthClient pointing to your auth Lambda
    auth = AuthClient(
        auth_url="https://jeamkhnl5r45vmustxn5xd6zjq0jjvkd.lambda-url.us-west-2.on.aws/login",
        username="test_user",
        password="test_password",
        logger=logger
    )

    # Unstable API client
    api_client = UnstableAPIClient(
        base_url="https://iykyuwuubdpdc7ktieifrs4jse0hzxhe.lambda-url.us-west-2.on.aws//data",
        auth_client=auth,
        logger=logger
    )

    # ApiDataService with mock storage
    storage_service = MockStorageService()
    api_service = ApiDataService(
        api_client=api_client,
        storage_service=storage_service,
        logger=logger
    )

    # Fetch data
    df = api_service.fetch_all_to_df(limit=3)

    # Assertions
    assert not df.empty, "DataFrame should not be empty"
    assert api_client.successful_pages > 0, "Should have successful pages"
    assert api_client.records_ingested == len(df), "Record count should match DataFrame length"

    # Upload to mock storage
    api_service.fetch_all_to_storage(bucket="mock-bucket", key="test_upload", format="csv")
