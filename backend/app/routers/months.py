import csv
import io
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, status
from fastapi.responses import Response

from app.models.month import MonthEntry
from app.models.settings import Settings
from app.schemas.month import MonthCreate, MonthUpdate, MonthResponse, ImportResult
from app.services.calculations import build_responses

_MONTH_NAMES = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4,
    'maggio': 5, 'giugno': 6, 'luglio': 7, 'agosto': 8,
    'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12,
}

router = APIRouter(prefix="/months", tags=["months"])


async def _initial_net_worth() -> float:
    doc = await Settings.find_one()
    return doc.initial_net_worth if doc else 0.0


async def _all_responses() -> list[MonthResponse]:
    entries = await MonthEntry.find_all().to_list()
    inw = await _initial_net_worth()
    return build_responses(entries, inw)


def _find_response(
    responses: list[MonthResponse], year: int, month: int
) -> MonthResponse | None:
    for r in responses:
        if r.year == year and r.month == month:
            return r
    return None


@router.get("/", response_model=list[MonthResponse])
async def list_months():
    responses = await _all_responses()
    return list(reversed(responses))


@router.get("/{year}/{month}", response_model=MonthResponse)
async def get_month(year: int, month: int):
    responses = await _all_responses()
    resp = _find_response(responses, year, month)
    if not resp:
        raise HTTPException(status_code=404, detail=f"{year}-{month:02d} not found")
    return resp


@router.post("/", response_model=MonthResponse, status_code=status.HTTP_201_CREATED)
async def create_month(payload: MonthCreate):
    existing = await MonthEntry.find_one(
        MonthEntry.year == payload.year, MonthEntry.month == payload.month
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Entry for {payload.year}-{payload.month:02d} already exists",
        )
    entry = MonthEntry(**payload.model_dump())
    await entry.insert()
    responses = await _all_responses()
    return _find_response(responses, payload.year, payload.month)


@router.put("/{year}/{month}", response_model=MonthResponse)
async def update_month(year: int, month: int, payload: MonthUpdate):
    entry = await MonthEntry.find_one(
        MonthEntry.year == year, MonthEntry.month == month
    )
    if not entry:
        raise HTTPException(status_code=404, detail=f"{year}-{month:02d} not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if update_data:
        await entry.set(update_data)

    responses = await _all_responses()
    return _find_response(responses, year, month)


@router.delete("/{year}/{month}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_month(year: int, month: int):
    entry = await MonthEntry.find_one(
        MonthEntry.year == year, MonthEntry.month == month
    )
    if not entry:
        raise HTTPException(status_code=404, detail=f"{year}-{month:02d} not found")
    await entry.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/import/csv", response_model=ImportResult)
async def import_csv(
    file: UploadFile = File(...),
    on_conflict: str = Query("upsert", pattern="^(upsert|skip)$"),
):
    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    imported = updated = skipped = 0
    errors: list[str] = []
    # (year*100+month, net_worth, net_worth_delta) for deriving initial net worth
    earliest: tuple[int, float, float] | None = None

    for i, row in enumerate(reader, start=2):
        try:
            row = {k.strip().lower().replace(" ", "_"): v.strip() for k, v in row.items() if k}

            year = int(row["year"])

            month_raw = row["month"]
            try:
                month = int(month_raw)
            except ValueError:
                month = _MONTH_NAMES.get(month_raw.lower())
                if not month:
                    raise ValueError(f"unrecognized month value: {month_raw!r}")

            income = float(row["income"])
            expenses = float(row["expenses"])
            investments = float(row.get("investments") or 0)
            pv_raw = row.get("portfolio_value", "")
            portfolio_value = float(pv_raw) if pv_raw else None
            notes_raw = row.get("notes", "")
            notes = notes_raw.strip('"') or None

            # track earliest row that carries net_worth + net_worth_delta
            try:
                nw = float(row["net_worth"])
                nw_delta = float(row["net_worth_delta"])
                key = year * 100 + month
                if earliest is None or key < earliest[0]:
                    earliest = (key, nw, nw_delta)
            except (KeyError, ValueError):
                pass

            existing = await MonthEntry.find_one(
                MonthEntry.year == year, MonthEntry.month == month
            )

            if existing:
                if on_conflict == "skip":
                    skipped += 1
                    continue
                await existing.set({
                    "income": income,
                    "expenses": expenses,
                    "investments": investments,
                    "portfolio_value": portfolio_value,
                    "notes": notes,
                })
                updated += 1
            else:
                await MonthEntry(
                    year=year, month=month, income=income,
                    expenses=expenses, investments=investments,
                    portfolio_value=portfolio_value, notes=notes,
                ).insert()
                imported += 1

        except Exception as exc:
            errors.append(f"row {i}: {exc}")

    derived = round(earliest[1] - earliest[2], 2) if earliest else None
    return ImportResult(
        imported=imported, updated=updated, skipped=skipped,
        errors=errors, derived_initial_net_worth=derived,
    )
