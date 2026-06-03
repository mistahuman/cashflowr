from typing import Optional
from beanie import Document
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class MonthEntry(Document):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    income: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)
    investments: float = Field(..., ge=0)
    initial_net_worth: Optional[float] = Field(None)

    class Settings:
        name = "months"
        indexes = [
            IndexModel([("year", ASCENDING), ("month", ASCENDING)], unique=True)
        ]
