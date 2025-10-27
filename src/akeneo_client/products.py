from __future__ import annotations
from typing import AsyncIterator, Optional, Dict, Any
from .http import AkeneoClient
from .models import Page, Product

PRODUCTS_UUID = "/api/rest/v1/products-uuid"

async def list_products(client: AkeneoClient, limit: int = 100, pagination_type: str = "search_after") -> Page:
    params: Dict[str, Any] = {"limit": min(limit, 100)}
    if pagination_type:
        params["pagination_type"] = pagination_type
    r = await client.get(PRODUCTS_UUID, params=params)
    return Page.model_validate(r.json())

async def iter_products(client: AkeneoClient, limit: int = 100) -> AsyncIterator[Product]:
    page = await list_products(client, limit=limit)
    for item in page.items():
        yield item
    next_link = page.links.next.href if page.links.next else None
    while next_link:
        r = await client.get(next_link.replace(str(client.client.base_url), ""), params=None)
        page = Page.model_validate(r.json())
        for item in page.items():
            yield item
        next_link = page.links.next.href if page.links.next else None
