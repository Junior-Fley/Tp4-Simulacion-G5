from pydantic import BaseModel
from typing import Any

from DTO.SimulacionItem import SimulacionItem


class SimularResponse(BaseModel):
    items: list[SimulacionItem]
    page: int
    size: int
    total: int
    total_pages: int