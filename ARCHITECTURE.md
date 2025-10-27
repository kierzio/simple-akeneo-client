## Architecture

This project is a small, modular Akeneo client implemented with modern Python packaging and async IO.

### Modules

- `src/akeneo_client/config.py`
  - Loads environment variables from `.env` using `python-dotenv`.
  - Provides an immutable `Settings` dataclass and `get_settings()` accessor.

- `src/akeneo_client/auth.py`
  - Implements the Akeneo Connector flow using OAuth2 Password Grant via `/api/oauth/v1/token`.
  - Uses Basic Auth header `base64(client_id:client_secret)` and JSON payloads for `grant_type=password` and `grant_type=refresh_token`.
  - Returns a `Token` object and refreshes a couple of minutes before expiry.

- `src/akeneo_client/http.py`
  - Wraps `httpx.AsyncClient` in `AkeneoClient`.
  - Ensures a valid bearer token on each request; retries once on 401 after refreshing.
  - Timeout and `base_url` are configured from settings.
  - Note: Tenacity is included for retry strategies and can be attached around requests if needed in future iterations.

- `src/akeneo_client/products.py`
  - Provides `list_products()` and `iter_products()` for the UUID products API `/api/rest/v1/products-uuid`.
  - Iterates pages by following `page._links.next` until exhausted.

- `src/akeneo_client/cli.py`
  - `typer` CLI exposing:
    - `akeneo auth` — obtain a token to validate credentials.
    - `akeneo products` — stream products as JSON lines (demo-limited via `--max-items`).

### Flow

1. CLI command starts and constructs `AkeneoClient`.
2. First request ensures a token via `obtain_token()`.
3. Requests include `Authorization: Bearer <token>`.
4. On 401, client refreshes the token once and retries.
5. Product iteration follows `_links.next` for pagination.

### Packaging

- `pyproject.toml` declares dependencies and console script entry point `akeneo`.
- Install with `pip install .`; the CLI becomes available in the active environment.

### Future enhancements
- Attach `tenacity` retry policies to network calls for transient failures.
- Add more Akeneo endpoints and richer query parameters/filters.
- Structured logging and metrics.

