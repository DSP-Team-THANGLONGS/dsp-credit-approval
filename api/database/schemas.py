from typing import Union

from pydantic import BaseModel
import datetime


class RecordsBase(BaseModel):
    own_car: str
    own_realty: str
    income: float
    education: str
    family_status: str
    housing_type: str
    birthday: int
    employed_day: int
    occupation: str
    fam_members: int
    result: int
    date_prediction: datetime.date


class RecordCreate(RecordsBase):
    own_car: str
    own_realty: str
    income: float
    education: str
    family_status: str
    housing_type: str
    birthday: int
    employed_day: int
    occupation: str
    fam_members: int
    result: int
    date_prediction: datetime.date


class Record(RecordsBase):
    own_car: str
    own_realty: str
    income: float
    education: str
    family_status: str
    housing_type: str
    birthday: int
    employed_day: int
    occupation: str
    fam_members: int
    result: int
    date_prediction: datetime.date

    class Config:
        from_attributes = True
