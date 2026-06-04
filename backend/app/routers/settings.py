from fastapi import APIRouter

from app.models.settings import Settings
from app.schemas.settings import SettingsResponse, SettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])


async def _get_or_create() -> Settings:
    doc = await Settings.find_one()
    if doc is None:
        doc = Settings()
        await doc.insert()
    return doc


def _to_response(doc: Settings) -> SettingsResponse:
    return SettingsResponse(
        initial_net_worth=doc.initial_net_worth,
        life_target=doc.life_target,
        investment_target=doc.investment_target,
        tax_rate=doc.tax_rate,
    )


@router.get("/", response_model=SettingsResponse)
async def get_settings():
    return _to_response(await _get_or_create())


@router.put("/", response_model=SettingsResponse)
async def update_settings(payload: SettingsUpdate):
    doc = await _get_or_create()
    await doc.set(payload.model_dump())
    return SettingsResponse(**payload.model_dump())
