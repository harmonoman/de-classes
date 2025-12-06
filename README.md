# de-classes

A playground for building interconnected, object-oriented data engineering components.

This repo provides a clean, modular environment for experimenting with reusable ETL/ELT workflows, storage clients, pipeline orchestration, and other data engineering abstractions — all using simple, surface-level class design that keeps concepts clear and understandable.

## Project Goals

- Demonstrate how data engineering systems can be modeled as composable classes.
- Keep components separated into clear silos (API, storage, logging, pipelines, transforms, etc.).
- Maintain focus on architecture, not low-level optimization or premature complexity.
- Provide a sandbox for experimenting with maintainable DE patterns.
- Explore object-oriented designs commonly used in production systems (factory patterns, mixins, strategy patterns, interfaces, etc.).

The goal is conceptual clarity, not production-grade engineering — a place to see how the pieces of a DE system fit together.

## Project Structure
```
de-classes/
│
├── src/
│   ├── main.py                  # Entry point for quick experiments
│   ├── api/                     # API ingestion clients
│   │   └── auth_client.py       # AuthClient: handles API authentication & token refresh
│   ├── common/                  # Shared classes (Logger, base classes, exceptions)
│   │   └── logger/
│   │       └── app_logger.py    # Lightweight centralized logging
│   ├── storage/                 # S3/MinIO/PostgreSQL abstractions
│   ├── pipelines/               # ETL/ELT pipeline classes
│   ├── utils/                   # Misc helpers and shared tools
│   └── configs/                 # (Optional) config management
│
├── dev/                          # Optional dev scripts
│   └── lambda_auth_simulator.py  # Local Lambda simulation for testing AuthClient
│
├── tests/                        # Unit tests for each component
├── requirements.txt
└── README.md
```

## Logging Design (Simple, Code-Based)

Logging is intentionally lightweight, centralized, and self-contained.

Instead of introducing external config files (YAML, JSON, etc.), logging is configured in pure Python using the `AppLogger` class in `src/common/logger/app_logger.py`.

### AppLogger Features

- Console logs (DEBUG+)
- Rotating file logs (ERROR+)
- Human-readable and JSON-like formats
- Automatic creation of a `logs/` directory
- Prevention of duplicate handlers on repeated imports
- A simple, unified interface for all application components

### Example Usage

```
from common.app_logger import AppLogger

logger = AppLogger(__name__).get_logger()

logger.info("Starting API ingestion step...")
logger.error("Failed to connect to endpoint")
```

## Authentication (AuthClient + Lambda Simulator)

This repo now includes basic authentication tooling for experimenting with API clients that require tokens.

### AuthClient Features

- Automatic token request & refresh
- Handles token expiration gracefully
- Returns standard Authorization headers for protected endpoints
- Simple interface for experimentation with token-based APIs

### Example Usage
```
from api.auth_client import AuthClient
from common.logger.app_logger import AppLogger

logger = AppLogger("my_logger").get_logger()

auth = AuthClient(
    auth_url="https://your-lambda-url/",  # Replace with your Lambda Function URL
    username="test_user",
    password="test_password",
    logger=logger
)

token = auth.get_token()
print("Token:", token)
```

### Lambda Auth Simulator
For local testing, a fake auth API is provided in dev/lambda_auth_simulator.py:

- Simulates a /login endpoint returning access_token and expires_in
- Provides a /data protected endpoint that checks Authorization headers
- Can be deployed as a Lambda Function URL for integration testing

## Storage Architecture

The repo now includes fully modular storage abstractions to handle uploading and downloading structured data with pandas DataFrames.

### Storage Clients

- BaseS3Client – low-level S3-compatible client (AWS S3 or MinIO)
- S3Client – AWS S3 specialization with optional session/profile handling
- MinioClient – MinIO specialization with bucket management helpers

### Data Services

- StorageDataService – orchestrates storing and retrieving DataFrames in S3/MinIO
- DataFormatService – converts DataFrames to/from CSV, JSON, and Parquet bytes

### Example Usage
```
from storage.clients.s3_client import S3Client
from storage.services import StorageDataService
from storage.format import DataFormatService
from common.logger.app_logger import AppLogger
import pandas as pd

logger = AppLogger("storage_test").get_logger()

s3 = S3Client(logger, access_key="your_key", secret_key="your_secret")
fmt = DataFormatService()
storage = StorageDataService(s3, fmt, logger)

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
storage.upload_df(df, bucket="my-bucket", key="test.csv", format="csv")
downloaded_df = storage.download_df("my-bucket", "test.csv", format="csv")
```

## How This Repo Works

Each directory represents a distinct portion of a data engineering system.
Classes are designed to be:

- Composable – they plug into pipelines without modification
- Extensible – subclassing and overrides are easy
- Lightweight – no unnecessary frameworks
- Focused on architecture – not production edge cases

### Example flow:

- `AuthClient` → fetches tokens from API
- `StorageClient` → handles low-level byte operations
- `DataFormatService` → handles serialization/deserialization
- `StorageDataService` → high-level DataFrame orchestration
- `AppLogger` → provides structured, centralized logging

The purpose is to visualize how all these moving pieces interact.

## Running the Project

1. Create and activate a virtual environment
`python3 -m venv .venv`

    Activate it:
    `source .venv/bin/activate`

2. Install dependencies
`pip install -r requirements.txt`

3. Run the project
`python src/main.py`

4. Optionally, test AuthClient with the Lambda simulator:

- Deploy `dev/lambda_auth_simulator.py` as an AWS Lambda function with a Function URL.
- Point your `AuthClient`'s `auth_url` to that URL to simulate login and protected endpoints.
- Alternatively, you can write a small local test script that calls `lambda_handler(event, context)` directly with mock `event` dictionaries for `/login` and `/data`.

## Future Ideas

- Extend storage clients to Postgres or other DBs
- ETL pipeline abstractions
- MinIO → Postgres loaders
- Config injection system
- Logging mixins for pipelines
- Object storage orchestration layer
