# Akeneo Client (MVP)

Minimal, async CLI client for Akeneo PIM using the Connector flow.

## Features
- Async HTTP via `httpx`
- Models via `pydantic`
- CLI via `typer`
- Token handling (password grant) and auto-refresh
- Simple product pagination (UUID API)

## Requirements
- Python 3.11+
- An Akeneo instance and a Connector (client_id/client_secret)

## Quick start
1) Copy environment template and fill values:
```bash
cp .env.example .env
# Edit .env to include: AKENEO_BASE_URL, AKENEO_CLIENT_ID, AKENEO_CLIENT_SECRET, AKENEO_USERNAME, AKENEO_PASSWORD
```

2) Create a virtual environment and install:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

3) Verify the CLI:
```bash
akeneo --help
```

## Help System

All commands include built-in help via `--help`:

```bash
# Show all available commands
akeneo --help

# Show detailed help for a specific command
akeneo auth --help
akeneo products --help
akeneo download --help
```

The help text shows:
- Command description
- All available options with defaults
- Option descriptions and constraints

## Usage
Authenticate to verify credentials:
```bash
akeneo auth
```

Stream products (UUID API) as JSON lines (demo-limited):
```bash
akeneo products --limit 100 --max-items 50
```

Pipe to `jq` for readability:
```bash
akeneo products --max-items 10 | jq .
```

Download products to a JSON file:
```bash
akeneo download --output downloads/products.json --max-items 100
```

**Download command:**
- Automatically creates `downloads/` directory if it doesn't exist
- All outputs go to `downloads/` by default (git-ignored, never committed)
- Options:
  - `--output` — file path (default: `downloads/products.json`)
  - `--limit` — items per API page, max 100 (default: 100)
  - `--max-items` — total items to download (default: all)

**Examples:**
```bash
# Download 5 products (goes to downloads/products.json)
akeneo download --max-items 5

# Download all products with custom filename
akeneo download --output downloads/all-products.json

# Download 200 products with custom page size
akeneo download --output downloads/large-batch.json --limit 50 --max-items 200
```

## Environment variables
Values are loaded from `.env`