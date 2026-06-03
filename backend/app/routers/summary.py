from datetime import date
from fastapi import APIRouter

from app.models.month import MonthEntry
from app.models.settings import Settings
from app.schemas.month import AnnualSummaryResponse, TrendsResponse, MonthResponse
from app.services.calculations import build_responses

router = APIRouter(prefix="/summary", tags=["summary"])


async def _initial_net_worth() -> float:
    doc = await Settings.find_one()
    return doc.initial_net_worth if doc else 0.0


async def _all_responses() -> list[MonthResponse]:
    entries = await MonthEntry.find_all().to_list()
    inw = await _initial_net_worth()
    return build_responses(entries, inw)


@router.get("/annual/{year}", response_model=AnnualSummaryResponse)
async def annual_summary(year: int):
    all_responses = await _all_responses()
    year_months = [r for r in all_responses if r.year == year]

    total_income = sum(r.income for r in year_months)
    total_expenses = sum(r.expenses for r in year_months)
    total_investments = sum(r.investments for r in year_months)
    total_savings = sum(r.savings for r in year_months)

    rates = [r.savings_rate for r in year_months if r.savings_rate is not None]
    avg_savings_rate = round(sum(rates) / len(rates), 4) if rates else None

    best_month: MonthResponse | None = None
    worst_month: MonthResponse | None = None
    if year_months:
        best_month = max(year_months, key=lambda r: r.savings)
        worst_month = min(year_months, key=lambda r: r.savings)

    return AnnualSummaryResponse(
        year=year,
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        total_investments=round(total_investments, 2),
        total_savings=round(total_savings, 2),
        avg_savings_rate=avg_savings_rate,
        best_month=best_month,
        worst_month=worst_month,
    )


@router.get("/trends", response_model=TrendsResponse)
async def trends():
    today = date.today()
    all_responses = await _all_responses()

    months_needed: list[tuple[int, int]] = []
    y, m = today.year, today.month
    for _ in range(12):
        months_needed.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    months_needed.reverse()

    month_map = {(r.year, r.month): r for r in all_responses}
    result = [month_map[k] for k in months_needed if k in month_map]

    return TrendsResponse(months=result)
