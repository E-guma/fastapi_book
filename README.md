# FastAPI Book — Cryptid API

Learning project from the FastAPI book (chapter 8): a small, layered API for
cataloguing cryptids and the explorers who chase them, backed by SQLite.

## Requirements

- Python 3.13+ (the project is pinned to 3.14 in `.python-version`)
- [uv](https://docs.astral.sh/uv/)

## Setup

From the repository root:

```bash
uv sync
```

## Run the API

```bash
cd chpt_8/src
uv run uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive API docs.

## Run the tests

From the repository root:

```bash
uv run pytest
```

Each test gets a fresh temporary SQLite database through the
`CRYPTID_SQLITE_DB` environment variable, so tests never touch
`chpt_8/src/db/`.

## Project layout

```
chpt_8/src/
├── main.py       # FastAPI app, lifespan, health check
├── model/        # Pydantic schemas
├── data/         # SQLite queries, connection lifecycle, domain errors
├── service/      # business layer
├── web/          # HTTP routers
├── fake/         # in-memory stubs
└── tests/unit/   # data, model, service, and web tests
```

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `CRYPTID_SQLITE_DB` | `chpt_8/src/db/cryptid.db` | SQLite database path |

The database file and its tables are created automatically on startup.
