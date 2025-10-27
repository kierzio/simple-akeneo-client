## Agents Guide

Guidance for autonomous agents or AI pair-programming in Cursor.

### Repository layout
- `pyproject.toml` — packaging, deps, console script.
- `src/akeneo_client/` — client implementation (config, auth, http, products, cli).
- `.env.example` — environment template; copy to `.env`.
- `README.md`, `ARCHITECTURE.md` — documentation.

### Safe commands to run
```bash
# Create & activate virtualenv
python3 -m venv .venv && source .venv/bin/activate

# Install package (editable not required for MVP)
pip install --upgrade pip
pip install .

# Verify CLI
akeneo --help
akeneo auth
akeneo products --max-items 5
```

### Environment
- Copy `.env.example` to `.env` and fill values. The real `.env` is private to the user.
- Required keys: `AKENEO_BASE_URL`, `AKENEO_CLIENT_ID`, `AKENEO_CLIENT_SECRET`, `AKENEO_USERNAME`, `AKENEO_PASSWORD`.

### Entry points
- CLI: `akeneo` (installed via console script).
- Library: import `AkeneoClient` from `akeneo_client.http` for custom flows.

### Cautions
- Network calls depend on Akeneo connectivity and credentials; handle 401/403 gracefully.
- Do not commit secrets; `.env` is ignored via `.gitignore`.
- Long-running streams should be demo-limited with `--max-items` to avoid large output.

