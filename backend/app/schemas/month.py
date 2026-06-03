from typing import Optional
from pydantic import BaseModel, Field


class MonthCreate(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    income: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)
    investments: float = Field(..., ge=0)
    initial_net_worth: Optional[float] = Field(None)


class MonthUpdate(BaseModel):
    income: Optional[float] = Field(None, ge=0)
    expenses: Optional[float] = Field(None, ge=0)
    investments: Optional[float] = Field(None, ge=0)
    initial_net_worth: Optional[float] = Field(None)


class MonthResponse(BaseModel):
    id: str
    year: int
    month: int
    income: float
    expenses: float
    investments: float
    initial_net_worth: Optional[float]
    savings: float
    net_worth: float
    net_worth_delta: float
    savings_rate: Optional[float]
    investment_rate: Optional[float]
    wealth_building_rate: Optional[float]
    consistency_check: float
    rolling_avg_3m: float


class AnnualSummaryResponse(BaseModel):
    year: int
    total_income: float
    total_expenses: float
    total_investments: float
    total_savings: float
    avg_savings_rate: Optional[float]
    best_month: Optional[MonthResponse]
    worst_month: Optional[MonthResponse]


class TrendsResponse(BaseModel):
    months: list[MonthResponse]
