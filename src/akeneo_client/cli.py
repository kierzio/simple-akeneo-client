from __future__ import annotations
import asyncio
import json
import typer
from pathlib import Path
from rich import print as rprint
from .http import AkeneoClient
from .auth import obtain_token

app = typer.Typer(no_args_is_help=True, add_completion=False)

@app.command()
def auth():
    "Obtain a token to verify credentials."
    async def run():
        c = AkeneoClient()
        try:
            tok = await obtain_token(c.client)
            rprint({"access_token_preview": tok.access_token[:8] + "...", "expires_in_s": int(tok.expires_at) })
        finally:
            await c.close()
    asyncio.run(run())

@app.command("products")
def products(limit: int = typer.Option(100, help="Items per page (max 100)"),
             max_items: int = typer.Option(100, help="Stop after this many items (for demos)")):
    "Stream products (UUID API) as JSON lines."
    async def run():
        c = AkeneoClient()
        n = 0
        try:
            async for p in __import__("akeneo_client.products").products.iter_products(c, limit=limit):
                print(json.dumps(p.model_dump()))
                n += 1
                if n >= max_items:
                    break
        finally:
            await c.close()
    asyncio.run(run())

@app.command("download")
def download(output: str = typer.Option("downloads/products.json", help="Output JSON file path (relative to downloads/)"),
             limit: int = typer.Option(100, help="Items per page (max 100)"),
             max_items: int = typer.Option(None, help="Stop after this many items (None = all)")):
    "Download products to a JSON file in downloads/ directory."
    async def run():
        c = AkeneoClient()
        products_list = []
        n = 0
        try:
            # Ensure downloads directory exists
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            async for p in __import__("akeneo_client.products").products.iter_products(c, limit=limit):
                products_list.append(p.model_dump())
                n += 1
                rprint(f"[bold green]✓[/bold green] Downloaded {n} products...", end="\r")
                if max_items and n >= max_items:
                    break
            
            # Write to file
            with open(output_path, "w") as f:
                json.dump(products_list, f, indent=2)
            rprint(f"\n[bold blue]✓ Saved {n} products to[/bold blue] {output_path.absolute()}")
        finally:
            await c.close()
    asyncio.run(run())
