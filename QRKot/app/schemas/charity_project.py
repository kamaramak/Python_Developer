from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt
from pydantic.types import PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=5,
        max_length=100,
    )
    description: str = Field(
        ...,
        min_length=10,
    )
    full_amount: PositiveInt = Field(
        ...,
        examples=[1],
    )

    model_config = ConfigDict(extra="forbid")


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=5,
        max_length=100,
    )
    description: Optional[str] = Field(
        None,
        min_length=10,
    )
    full_amount: Optional[PositiveInt] = Field(
        None,
        examples=[1],
    )
