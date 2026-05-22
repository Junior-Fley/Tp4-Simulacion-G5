from pydantic import BaseModel
from typing import Any

class SimularResponse(BaseModel):
    items: list[dict[str, Any]]
    page: int
    size: int
    total: int
    total_pages: int