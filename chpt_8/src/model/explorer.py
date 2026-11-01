from pydantic import BaseModel, Field


class Explorer(BaseModel):
    name: str = Field(min_length=1)
    country: str
    description: str
