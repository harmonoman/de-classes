import requests
from src.common.logger.app_logger import AppLogger
from src.api.auth_client import AuthClient


def main():

    logger = AppLogger("my_logger").get_logger()

    auth = AuthClient(
        auth_url="https://esvceo3iqxuizd2pmtmg5av4s40yamby.lambda-url.us-west-2.on.aws/login",
        username="test_user",
        password="test_password",
        logger=logger
    )

    token = auth.get_token()
    print("Token:", token)

    # Example of calling a protected endpoint
    response = requests.get(
        "https://esvceo3iqxuizd2pmtmg5av4s40yamby.lambda-url.us-west-2.on.aws/data",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    main()
