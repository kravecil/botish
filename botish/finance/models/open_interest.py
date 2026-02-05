from datetime import datetime
from pydantic import BaseModel


class OpenInterest(BaseModel):
    symbol: str
    value: float
    dt: datetime
