from fastapi import APIRouter

from app.models.settings import Settings
from app.schemas.settings import SettingsResponse, SettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])


async def _get_or_create() -> Settings:
    doc = await Settings.find_one()
    if doc is None:
        doc = Settings(initial_net_worth=0.0)
        await doc.insert()
    return doc


@router.get("/", response_model=SettingsResponse)
async def get_settings():
    doc = await _get_or_create()
    return SettingsResponse(initial_net_worth=doc.initial_net_worth)


@router.put("/", response_model=SettingsResponse)
async def update_settings(payload: SettingsUpdate):
    doc = await _get_or_create()
    await doc.set({"initial_net_worth": payload.initial_net_worth})
    return SettingsResponse(initial_net_worth=payload.initial_net_worth)
