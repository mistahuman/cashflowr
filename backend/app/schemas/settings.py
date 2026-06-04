from pydantic import BaseModel


class SettingsResponse(BaseModel):
    initial_net_worth: float
    life_target: float
    investment_target: float
    tax_rate: float


class SettingsUpdate(BaseModel):
    initial_net_worth: float
    life_target: float
    investment_target: float
    tax_rate: float
