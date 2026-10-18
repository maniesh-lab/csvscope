from pydantic import BaseModel
from typing import Optional


class AnalysisResponse(BaseModel):
    filename: str
    rows: int
    stats: dict
    chart: Optional[str] = None
    message: Optional[str] = None  # explains why there's no chart, when there isn't one