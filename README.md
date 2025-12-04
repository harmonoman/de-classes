# de-classes

A playground for building interconnected, object-oriented data engineering components.

This repo provides a clean, modular environment for experimenting with reusable ETL/ELT workflows, API wrappers, storage clients, pipeline orchestration, and other data engineering abstractions — all using simple, surface-level class design that keeps concepts clear and understandable.

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
│   ├── main.py              # Entry point for quick experiments
│   ├── api/                 # API ingestion clients
│   ├── common/              # Shared classes (Logger, base classes, exceptions)
│   ├── storage/             # S3/MinIO/PostgreSQL abstractions
│   ├── pipelines/           # ETL/ELT pipeline classes
│   ├── utils/               # Misc helpers and shared tools
│   └── configs/             # (Optional) config management
│
├── tests/                   # Unit tests for each component
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

Each component in the repo gets its own namespaced logger automatically, helping you see how logging spreads through a pipeline without getting stuck in configuration complexity.

## How This Repo Works

Each directory represents a distinct portion of a data engineering system.
Classes are designed to be:

- Composable – they plug into pipelines without modification
- Extensible – subclassing and overrides are easy
- Lightweight – no unnecessary frameworks
- Focused on architecture – not production edge cases

### Example flow:

- `ApiClient` → fetches data
- `StorageClient` → writes to S3 / Minio / Postgres
- `Pipeline` → coordinates extract → transform → load
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

## Future Ideas

- API client with rate-limiting & retries
- Base ETL pipeline class
- Postgres → S3 or MinIO sync
- MinIO → Postgres loader
- Object storage abstraction layer
- Config injection system
- Logging mixins for pipelines
- Random number generator API client (for testing ingestion flows)

## Branch: project-setup

This branch establishes:

- the initial class-based structure
- logging as a clean, isolated component
- folder layout for future DE objects

It serves as the foundation for all future components and experiments.

