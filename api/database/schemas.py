from pydantic import BaseModel
import datetime


class RecordsBase(BaseModel):
    own_car: str
    own_realty: str
    income: float
    education: str
    family_status: str
    housing_type: str
    birthday: datetime.date
    employed_day: datetime.date
    still_working: bool
    occupation: str
    fam_members: int
    result: int
    platform: str
    date_prediction: datetime


class RecordCreate(RecordsBase):
    own_car: str
    own_realty: str
    income: float
    education: str
    family_status: str
    housing_type: str
    birthday: datetime.date
    employed_day: datetime.date
    still_working: bool
    occupation: str
    fam_members: int
    result: int
    platform: str
    date_prediction: datetime


class Record(RecordsBase):
    own_car: str
    own_realty: str
    income: float
    education: str
    family_status: str
    housing_type: str
    birthday: datetime.date
    employed_day: datetime.date
    still_working: bool
    occupation: str
    fam_members: int
    result: int
    platform: str
    date_prediction: datetime

    class Config:
        from_attributes = True
