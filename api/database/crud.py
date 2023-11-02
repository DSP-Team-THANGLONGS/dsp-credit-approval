from sqlalchemy.orm import Session

from . import models

import numpy as np
from psycopg2.extensions import register_adapter, AsIs

register_adapter(np.int64, AsIs)


def get_records(db: Session, limit: int = 100):
    records = db.query(models.Records).limit(limit).all()
    return records


def save_record(db: Session, record: dict):
    db_record = models.Records(
        own_car=record["own_car"],
        own_realty=record["own_realty"],
        income=record["income"],
        education=record["education"],
        family_status=record["family_status"],
        housing_type=record["housing_type"],
        birthday=record["birthday"],
        employed_day=record["employed_day"],
        occupation=record["occupation"],
        still_working=record["still_working"],
        fam_members=record["fam_members"],
        result=record["result"],
        date_prediction=record["date_prediction"],
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
