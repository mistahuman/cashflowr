from app.models.month import MonthEntry
from app.schemas.month import MonthResponse


def _rate(numerator: float, income: float) -> float | None:
    if income == 0:
        return None
    return round(numerator / income * 100, 4)


def compute_derived(
    entry: MonthEntry,
    prev_net_worth: float,
    last_3_incomes: list[float],
) -> dict:
    savings = round(entry.income - entry.expenses - entry.investments, 10)
    net_worth = round(prev_net_worth + savings + entry.investments, 10)
    net_worth_delta = round(net_worth - prev_net_worth, 10)

    savings_rate = _rate(savings, entry.income)
    investment_rate = _rate(entry.investments, entry.income)
    wealth_building_rate = _rate(savings + entry.investments, entry.income)

    consistency_check = round(net_worth_delta - (savings + entry.investments), 10)

    rolling_avg_3m = round(sum(last_3_incomes) / len(last_3_incomes), 10) if last_3_incomes else 0.0

    return {
        "savings": savings,
        "net_worth": net_worth,
        "net_worth_delta": net_worth_delta,
        "savings_rate": savings_rate,
        "investment_rate": investment_rate,
        "wealth_building_rate": wealth_building_rate,
        "consistency_check": consistency_check,
        "rolling_avg_3m": rolling_avg_3m,
    }


def build_responses(entries: list[MonthEntry]) -> list[MonthResponse]:
    """
    Process entries in chronological order, threading net_worth and rolling incomes.
    Returns MonthResponse objects in the same order as input.
    """
    sorted_entries = sorted(entries, key=lambda e: (e.year, e.month))
    results: dict[tuple[int, int], MonthResponse] = {}
    prev_net_worth: float = 0.0
    income_history: list[float] = []

    for entry in sorted_entries:
        if entry.initial_net_worth is not None and not results:
            prev_net_worth = entry.initial_net_worth

        income_history.append(entry.income)
        last_3 = income_history[-3:]

        derived = compute_derived(entry, prev_net_worth, last_3)
        prev_net_worth = derived["net_worth"]

        resp = MonthResponse(
            id=str(entry.id),
            year=entry.year,
            month=entry.month,
            income=entry.income,
            expenses=entry.expenses,
            investments=entry.investments,
            initial_net_worth=entry.initial_net_worth,
            **derived,
        )
        results[(entry.year, entry.month)] = resp

    return [results[k] for k in sorted(results.keys())]
