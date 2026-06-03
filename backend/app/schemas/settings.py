from pydantic import BaseModel


class SettingsResponse(BaseModel):
    initial_net_worth: float


class SettingsUpdate(BaseModel):
    initial_net_worth: float
