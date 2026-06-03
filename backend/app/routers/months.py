from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from app.models.month import MonthEntry
from app.models.settings import Settings
from app.schemas.month import MonthCreate, MonthUpdate, MonthResponse
from app.services.calculations import build_responses

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
