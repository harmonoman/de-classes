import json
import base64
import time
import random

# -------------------------------
# Auth config
# -------------------------------
VALID_USERNAME = "test_user"
VALID_PASSWORD = "test_password"


def generate_token(username):
    """Generate a fake token using base64 + timestamp."""
    payload = f"{username}:{int(time.time())}"
    return base64.urlsafe_b64encode(payload.encode()).decode()


# -------------------------------
# API config
# -------------------------------
TOTAL_PAGES = 5
PAGE_SIZE = 3
FAIL_RATE_500 = 0.2   # 20% chance
FAIL_RATE_429 = 0.3   # 10% chance


# -------------------------------
# Endpoint handlers
# -------------------------------
def handle_login(body):
    username = body.get("username")
    password = body.get("password")

    if username != VALID_USERNAME or password != VALID_PASSWORD:
        return 401, {"error": "Invalid credentials"}

    return 200, {
        "access_token": generate_token(username),
        "expires_in": 3600
    }


def handle_data(headers, query_params):
    # Auth check
    auth = headers.get("authorization") or headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return 401, {"error": "Missing or invalid token"}

    # Random failures
    r = random.random()
    if r < FAIL_RATE_500:
        return 500, {"error": "Server error"}
    elif r < FAIL_RATE_500 + FAIL_RATE_429:
        return 429, {"error": "Rate limited"}

    # Paginated response
    page = int(query_params.get("page", 1))
    if page > TOTAL_PAGES or page < 1:
        return 404, {"error": "Page not found"}

    data = [{"id": f"{page}-{i}", "value": random.randint(1, 100)} for i in range(PAGE_SIZE)]
    response = {
        "metadata": {"total_pages": TOTAL_PAGES},
        "data": data
    }
    return 200, response


# -------------------------------
# Lambda handler
# -------------------------------
def lambda_handler(event, context):
    path = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    headers = event.get("headers", {})
    query_params = event.get("queryStringParameters") or {}

    try:
        body = json.loads(event["body"]) if event.get("body") else {}

        if path == "/login" and method == "POST":
            status, result = handle_login(body)
        elif path == "/data" and method == "GET":
            status, result = handle_data(headers, query_params)
        else:
            status, result = 404, {"error": "Not found"}

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
