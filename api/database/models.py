from .database import Base
from sqlalchemy import Column, Date, Integer, String, Float, Boolean


class Records(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    own_car = Column(String, index=True)
    own_realty = Column(String, index=True)
    income = Column(Float)
    education = Column(String, index=True)
    family_status = Column(String, index=True)
    housing_type = Column(String, index=True)
    birthday = Column(Date)
    employed_day = Column(Date)
    still_working = Column(Boolean)
    occupation = Column(String, index=True)
    fam_members = Column(Integer)
    result = Column(Integer)
    date_prediction = Column(Date)
