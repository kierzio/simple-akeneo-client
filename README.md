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
akeneo download --filename products.json --max-items 100
```

**Download command:**
- **All files are saved to `downloads/` directory** (cannot be overridden)
- Automatically creates `downloads/` directory if it doesn't exist
- Git-ignored, never committed
- Options:
  - `--filename` — filename only (saved to downloads/) (default: `products.json`)
  - `--limit` — items per API page, max 100 (default: 100)
  - `--max-items` — total items to download (default: all)

**Examples:**
```bash
# Download 5 products to downloads/products.json
akeneo download --max-items 5

# Download all products with custom filename to downloads/
akeneo download --filename all-products.json

# Download 200 products with custom page size to downloads/
akeneo download --filename large-batch.json --limit 50 --max-items 200
```

## Environment variables
Values are loaded from `.env`:
- `AKENEO_BASE_URL` — Base URL of your Akeneo instance (e.g., `https://akeneo.example.com`)
- `AKENEO_CLIENT_ID` — OAuth2 client ID (from Connector)
- `AKENEO_CLIENT_SECRET` — OAuth2 client secret (from Connector)
- `AKENEO_USERNAME` — Username for password grant
- `AKENEO_PASSWORD` — Password for password grant