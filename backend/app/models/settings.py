from beanie import Document
from pydantic import Field


class Settings(Document):
    initial_net_worth: float = Field(default=0.0)
    life_target: float = Field(default=0.0)
    investment_target: float = Field(default=0.0)
    tax_rate: float = Field(default=0.0)   # percentage, e.g. 15.0 for forfettario

    class Settings:
        name = "settings"
