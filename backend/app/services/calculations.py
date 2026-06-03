from app.models.month import MonthEntry
from app.schemas.month import MonthResponse


def _rate(numerator: float, income: float) -> float | None:
    if income == 0:
        return None
    return round(numerator / income * 100, 4)


def compute_derived(
    entry: MonthEntry,
    prev_liquid: float,
    prev_portfolio: float,
    last_3_incomes: list[float],
) -> dict:
    savings = round(entry.income - entry.expenses - entry.investments, 10)
    liquid_balance = round(prev_liquid + savings, 10)

    # Usa il valore portafoglio inserito questo mese, altrimenti porta avanti l'ultimo noto
    portfolio_value_effective = entry.portfolio_value if entry.portfolio_value is not None else prev_portfolio

    net_worth = round(liquid_balance + portfolio_value_effective, 10)
    prev_net_worth = round(prev_liquid + prev_portfolio, 10)
    net_worth_delta = round(net_worth - prev_net_worth, 10)

    savings_rate = _rate(savings, entry.income)
    investment_rate = _rate(entry.investments, entry.income)
    wealth_building_rate = _rate(entry.income - entry.expenses, entry.income)

    rolling_avg_3m = round(sum(last_3_incomes) / len(last_3_incomes), 10) if last_3_incomes else 0.0

    return {
        "savings": savings,
        "liquid_balance": liquid_balance,
        "portfolio_value_effective": portfolio_value_effective,
        "net_worth": net_worth,
        "net_worth_delta": net_worth_delta,
        "savings_rate": savings_rate,
        "investment_rate": investment_rate,
        "wealth_building_rate": wealth_building_rate,
        "rolling_avg_3m": rolling_avg_3m,
    }


def build_responses(entries: list[MonthEntry], initial_net_worth: float = 0.0) -> list[MonthResponse]:
    sorted_entries = sorted(entries, key=lambda e: (e.year, e.month))
    results: dict[tuple[int, int], MonthResponse] = {}
    prev_liquid: float = initial_net_worth
    prev_portfolio: float = 0.0
    income_history: list[float] = []

    for entry in sorted_entries:
        income_history.append(entry.income)
        last_3 = income_history[-3:]

        derived = compute_derived(entry, prev_liquid, prev_portfolio, last_3)

        prev_liquid = derived["liquid_balance"]
        prev_portfolio = derived["portfolio_value_effective"]

        resp = MonthResponse(
            id=str(entry.id),
            year=entry.year,
            month=entry.month,
            income=entry.income,
            expenses=entry.expenses,
            investments=entry.investments,
            portfolio_value=entry.portfolio_value,
            notes=entry.notes,
            **derived,
        )
        results[(entry.year, entry.month)] = resp

    return [results[k] for k in sorted(results.keys())]
