from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.types import NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    full_amount: NonNegativeInt
    comment: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationBase):
    id: int
    create_date: datetime


class DonationFullInfoDB(DonationDB):
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime] = None
    user_id: int
