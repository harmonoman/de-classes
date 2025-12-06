import requests
from src.common.logger.app_logger import AppLogger
from src.api.auth_client import AuthClient
from tests.test_storage import test_storage
from tests.test_unstable_api import test_unstable_api_integration


def main():

    logger = AppLogger("my_logger").get_logger()

    auth = AuthClient(
        auth_url="https://jeamkhnl5r45vmustxn5xd6zjq0jjvkd.lambda-url.us-west-2.on.aws/login",
        username="test_user",
        password="test_password",
        logger=logger
    )

    token = auth.get_token()
    print("Token:", token)

    # Example of calling a protected endpoint
    response = requests.get(
        "https://jeamkhnl5r45vmustxn5xd6zjq0jjvkd.lambda-url.us-west-2.on.aws/data",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.status_code)
    print(response.json())

    test_storage(logger)

    test_unstable_api_integration(logger)


if __name__ == '__main__':
    main()
