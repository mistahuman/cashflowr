from typing import Optional
from pydantic import BaseModel, Field


class MonthCreate(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    income: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)
    investments: float = Field(default=0.0)
    portfolio_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None)


class MonthUpdate(BaseModel):
    income: Optional[float] = Field(None, ge=0)
    expenses: Optional[float] = Field(None, ge=0)
    investments: Optional[float] = Field(None)
    portfolio_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None)


class MonthResponse(BaseModel):
    id: str
    year: int
    month: int
    income: float
    expenses: float
    investments: float
    portfolio_value: Optional[float]       # valore grezzo inserito (None = non impostato questo mese)
    portfolio_value_effective: float       # valore effettivo usato (carry-forward se None)
    notes: Optional[str]
    savings: float
    liquid_balance: float
    net_worth: float                       # liquid_balance + portfolio_value_effective
    net_worth_delta: float
    savings_rate: Optional[float]
    investment_rate: Optional[float]
    wealth_building_rate: Optional[float]
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


class ImportResult(BaseModel):
    imported: int
    updated: int
    skipped: int
    errors: list[str]
    derived_initial_net_worth: Optional[float] = None
