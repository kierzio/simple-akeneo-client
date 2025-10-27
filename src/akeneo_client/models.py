from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, List, Optional

class Link(BaseModel):
    href: str

class Links(BaseModel):
    self: Link
    first: Optional[Link] = None
    next: Optional[Link] = None
    previous: Optional[Link] = None

class Product(BaseModel):
    # Keep loose for MVP; you can tighten later per your catalog
    identifier: Optional[str] = None
    uuid: Optional[str] = None
    enabled: Optional[bool] = None
    family: Optional[str] = None
    values: Dict[str, Any] = Field(default_factory=dict)

class Page(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    links: Links = Field(alias="_links")
    embedded: Dict[str, List[Product]] = Field(default_factory=dict, alias="_embedded")

    def items(self) -> List[Product]:
        return [Product.model_validate(i) for i in self.embedded.get("items", [])]
