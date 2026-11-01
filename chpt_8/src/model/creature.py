from pydantic import BaseModel, Field


class Creature(BaseModel):
    name: str = Field(min_length=1)
    country: str
    area: str
    description: str
    aka: str
