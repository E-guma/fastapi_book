from pydantic import BaseModel, Field, ConfigDict


class Creature(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    country: str
    area: str
    description: str
    aka: str
