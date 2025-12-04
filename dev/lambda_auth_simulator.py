import json
import base64
import time

VALID_USERNAME = "test_user"
VALID_PASSWORD = "test_password"


def generate_token(username):
    payload = f"{username}:{int(time.time())}"
    return base64.urlsafe_b64encode(payload.encode()).decode()


def handle_login(body):
    username = body.get("username")
    password = body.get("password")

    if username != VALID_USERNAME or password != VALID_PASSWORD:
        return 401, {"error": "Invalid credentials"}

    return 200, {
        "access_token": generate_token(username),
        "expires_in": 3600
    }


def handle_data(headers):
    auth = headers.get("authorization") or headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return 401, {"error": "Missing or invalid token"}

    token = auth.split(" ")[1]
    return 200, {"message": "Protected data", "token_received": token}


def lambda_handler(event, context):
    path = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    try:
        body = json.loads(event["body"]) if event.get("body") else {}

        if path == "/login" and method == "POST":
            status, result = handle_login(body)
        elif path == "/data" and method == "GET":
            headers = event.get("headers", {})
            status, result = handle_data(headers)
        else:
            status, result = (404, {"error": "Not found"})

        return {
            "statusCode": status,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
