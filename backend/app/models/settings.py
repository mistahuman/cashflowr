from beanie import Document
from pydantic import Field


class Settings(Document):
    initial_net_worth: float = Field(default=0.0)

    class Settings:
        name = "settings"
