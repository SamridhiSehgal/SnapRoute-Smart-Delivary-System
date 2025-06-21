from pydantic import BaseModel
from typing import List

class PathRequest(BaseModel):
    start: str
    end: str
    k: int = 3

class DijkstraResponse(BaseModel):
    cost: int
    path: List[str]

class KPathsResponse(BaseModel):
    paths: List[dict]  # Each dict: {'cost': int, 'path': List[str]}
