# de-classes

A playground for building **interconnected, object-oriented data engineering components**.  
This repo is designed to help experiment with reusable ETL/ELT workflows, API wrappers, storage clients, pipeline orchestration, and other data engineering abstractions — all using clean, extensible class design.

---

## Project Goals

- Demonstrate how data engineering systems can be modeled as composable classes.
- Make each component (API ingestion, S3/MinIO client, PostgreSQL connector, pipelines, transforms, etc.) modular and testable.
- Provide a sandbox for experimenting with maintainable DE architectures.
- Explore design patterns commonly used in production pipelines (factory patterns, mixins, strategy patterns, interfaces, etc.).

---

## Project Structure
```
de-classes/
│
├── src/
│ ├── main.py # Entry point for local testing
│ ├── api/ # API ingestion clients
│ ├── storage/ # S3/MinIO/PostgreSQL abstractions
│ ├── pipelines/ # ETL/ELT pipeline classes
│ ├── utils/ # Helpers, logging, shared tools
│ └── configs/ # Config management
│
├── tests/ # Unit tests for all components
├── requirements.txt
└── README.md
```

---

## How This Repo Works

Each directory corresponds to a category of DE functionality.  
Classes should be:

- **Composable** (easy to plug into pipelines)
- **Extensible** (easy to override and expand)
- **Pure Python** (no heavy frameworks unless needed)
- **Focused** on demonstrating DE architecture patterns

Example:  
- `ApiClient` → fetches data  
- `StorageClient` → writes to S3 / Minio / Postgres  
- `Pipeline` → orchestrates extract → transform → load steps  

---

## Running the Project

`python src/main.py`

Eventually, each class will be runnable independently for isolated experimentation.

---

## Future Ideas

- API rate-limiting + retry logic class
- Generic ETL pipeline superclass
- Postgres → S3 sync class
- MinIO → Postgres loader
- Object storage abstraction layer
- Config injection system
- Class-based workflow logging
- Class to return random numbers (for testing API wrappers)

---

## Branch: project-setup

This branch establishes the initial structure and serves as the foundation for all future class development.

---