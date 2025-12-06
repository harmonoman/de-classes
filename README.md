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
│   ├── main.py                        # Entry point for quick experiments
│
│   ├── api/
│   │   ├── auth_client.py             # AuthClient: token-based API authentication
│   │   ├── unstable_api_client.py     # Client w/ retries, backoff, pagination for unstable APIs
│   │   └── api_data_service.py        # High-level ingestion: fetches all pages to DF or storage
│
│   ├── common/
│   │   └── logger/
│   │       └── app_logger.py          # Lightweight centralized logging utility
│
│   ├── storage/
│   │   ├── clients/                   # S3, MinIO, and base storage clients
│   │   ├── services/                  # High-level DataFrame upload/download orchestration
│   │   └── format/                    # CSV/JSON/Parquet serialization helpers
│
│   ├── pipelines/                     # ETL/ELT pipeline classes
│   ├── utils/                         # Shared utilities
│   └── configs/                       # Optional config management
│
├── dev/
│   ├── lambda_auth_simulator.py       # Auth + protected endpoint simulator
│   └── unstable_api_simulator.py      # New: unstable API simulator w/ 429, 500, jittery failures
│
├── tests/                             # Tests for API, storage, and pipeline components
├── requirements.txt
└── README.md
```

## Logging Design (Simple, Code-Based)

Logging is lightweight, centralized, and fully Pythonic — no YAML or heavy config systems.

### AppLogger Features

- Console logs (DEBUG+)
- Rotating file logs (ERROR+)
- Consistent, readable formatting
- Auto-created logs/ directory
- No duplicate handlers on re-import
- Plug-and-play for all modules

### Example Usage

```
from common.logger.app_logger import AppLogger
logger = AppLogger("demo").get_logger()

logger.info("Starting an ingestion task...")
logger.error("Something went wrong")
```

## Authentication (AuthClient + Lambda Simulator)

The repo includes a fully self-contained authentication stack for simulating token-based APIs.

### AuthClient Features

- Automatic token request & refresh
- Handles token expiration gracefully
- Returns standard Authorization headers for protected endpoints
- Simple interface for experimentation with token-based APIs

### Example Usage
```
from api.auth_client import AuthClient
from common.logger.app_logger import AppLogger

logger = AppLogger("auth_test").get_logger()

auth = AuthClient(
    auth_url="https://your-lambda-url/login",
    username="test_user",
    password="test_password",
    logger=logger
)

token = auth.get_token()
print("Token:", token)
```

### Lambda Auth Simulator (`dev/lambda_auth_simulator.py`)

For local testing, a fake auth API is provided in `dev/lambda_auth_simulator.py`:

- `/login` — returns `access_token` + `expires_in`
- `/data` — checks `Authorization: Bearer <token>`
- Useful for testing `AuthClient` without real API dependencies

## Unstable API Ingestion
(`unstable_api_client.py` + `unstable_api_simulator.py`)

This module pair simulates a chaotic real-world service and a client designed to survive it.

### `unstable_api_simulator.py` Features

- Random 500, 503, and 429 failures
- Random jitter
- Pagination with total_pages
- Token-required /data endpoint
- Configurable fail rates

### UnstableAPIClient Features

- Automatic retry w/ exponential backoff
- Optional jitter
- Handles:
    * 429 (rate limit)
    * 500/503 (server failure)
    * network-level errors
- Tracks:
    * retry_count
    * successful_pages
    * failed_pages
    * records_ingested
- Clean generator interface:
`for page_num, result in api_client.iterate_all_pages(limit=100):`

## High-Level API Ingestion
`api_data_service.py`

A service layer that converts paginated API responses into either:

- a DataFrame, or
- uploaded artifacts in S3/MinIO.

### Features

- Fetch all pages with reuse of `UnstableAPIClient`
- Safe handling of empty pages or retries
- Concatenates into a unified DataFrame
- Uploads as CSV, JSON, or Parquet via StorageDataService

### Example
```
df = data_service.fetch_all_to_df(limit=100)
data_service.fetch_all_to_storage(
    bucket="raw",
    key="unstable_data.csv",
    format="csv"
)
```

## Storage Architecture

A modular set of clients designed to show how storage layers fit into an ETL workflow.

### Storage Clients

- `BaseS3Client` – low-level S3-compatible client (AWS S3 or MinIO)
- `S3Client` – AWS S3 specialization with optional session/profile handling
- `MinioClient` – MinIO specialization with bucket management helpers

### Data Services

- `StorageDataService` – orchestrates storing and retrieving DataFrames in S3/MinIO
- `DataFormatService` – converts DataFrames to/from CSV, JSON, and Parquet bytes

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

`AuthClient` → retrieves and refreshes tokens  
`UnstableAPIClient` → pulls pages w/ retries and jitter  
`ApiDataService` → collects into a DataFrame  
`DataFormatService` → converts to bytes  
`StorageDataService` → uploads to MinIO or S3  
`AppLogger` → logs every step consistently

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

4. (Optional) Test authentication or unstable API behavior

- Deploy the Lambda simulators (`dev/`)
- Or call their `lambda_handler()` functions locally with mock request events

## Future Ideas

- PostgreSQL storage + loaders
- More complete ETL pipelines
- Config injection system
- Pluggable transformations
- Logging mixins for pipelines
- Object storage orchestration layer
