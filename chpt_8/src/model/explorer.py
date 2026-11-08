from pydantic import BaseModel, Field, ConfigDict


class Explorer(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    country: str
    description: str
