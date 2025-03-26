from pydantic import BaseModel
from typing import List, Optional

class CurrencyBase(BaseModel):
    country: str
    currency: str
    abbreviation: str
    buy_rate: float
    sell_rate: float

class CurrencyCreate(CurrencyBase):
    pass  # Used for input validation

class CurrencyUpdate(BaseModel):
    buy_rate: Optional[float]
    sell_rate: Optional[float]

class CurrencyResponse(CurrencyBase):
    id: int

    class Config:
        from_attributes = True  # For ORM Mode in Pydantic
